# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Replay the exact 2026-07-22 YM literature into local theory production.

This module is deliberately narrower than the canonical discovery cycle.  It
reopens the checked-in capture, normalized acquisition, and six tool-visible
response files; then it executes every deterministic source-routing and theory
builder in the chain.  Both conceptual adjudications use the registered blind
operator, typed explanatory graphs, and three content-bearing deep lenses.  The
judges share local executable authority and are therefore recorded as an
explicitly correlated internal panel, never as external or independent review.

The resulting manifest is publication-disabled and cannot commission a world.
Its positive claim is local, bounded production causality: exact source bytes
were consumed in a strict order by identified code and dependency bytes.  It
does not establish source truth, global latestness, exhaustive coverage,
literature benefit, creativity, conceptual merit, physics value, a theorem, or
a Yang--Mills result.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence
from unittest.mock import patch

from agentic.discovery.conceptual_adjudication import (
    DIMENSIONS,
    build_adjudication_source_bindings,
    build_blind_packet,
    build_judge_report,
)
from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_payload,
)
from agentic.discovery.hypotheses import forge_high_risk_portfolio
from agentic.discovery.literature import (
    CLAIM_MAPPING_ALGORITHM_ID,
    assimilate_derived_literature,
    build_theory_object_catalog,
    derive_claim_mappings,
    validate_assimilation,
    validate_claim_mapping_derivation,
    validate_snapshot,
)
from agentic.discovery.literature_acquisition import (
    LiteratureAcquisitionError,
    build_source_routing_pre_map_policy,
    build_source_routing_realization,
    build_source_routing_warrant_validation_packet,
    load_tool_response_artifact,
    source_routing_realization_requirements,
    validate_capture_acquisition_bundle,
    validate_source_routing_pre_map_policy,
    validate_source_routing_realization,
    validate_source_routing_warrant_validation_packet,
)
from agentic.discovery.reflection import validate_packet_invariants
from agentic.scripts.run_discovery_operator_protocol import execute as execute_operator


CODE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_AUTHORITY_ROOT = Path(__file__).resolve().parent
SCHEMA_NAME = "literature_production_chain_manifest.schema.json"
SCHEMA_RELATIVE_PATH = f"agentic/spec/{SCHEMA_NAME}"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"
RUN_ID = "ym-literature-production-20260722"
STATE_VERSION = 0
CAPTURE_NAME = "frontier_search_live_capture_20260722.json"
ACQUISITION_NAME = "frontier_search_live_acquisition_20260722.json"
FRESHNESS_MAX_AGE_SECONDS = 2_592_000

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

_MODULE_PATH = (
    "agentic/evals/ym_representational_dynamics_20260721/"
    "literature_production_chain.py"
)
_OPERATOR_PROTOCOL_PATH = "agentic/scripts/run_discovery_operator_protocol.py"
_OPERATOR_REGISTRY_PATH = "agentic/registries/discovery_operator_registry.yaml"

_STAGE_IMPLEMENTATIONS: dict[str, tuple[str, str, tuple[str, ...]]] = {
    "acquisition_reopen": (
        "agentic.discovery.literature_acquisition:validate_capture_acquisition_bundle",
        "1.0.0",
        (
            "agentic/discovery/literature_acquisition.py",
            "agentic/discovery/literature.py",
            "agentic/discovery/contracts.py",
            "agentic/spec/ym_current_literature_capture.schema.json",
            "agentic/spec/literature_tool_response_artifact_v2.schema.json",
            "agentic/spec/literature_source_version_graph.schema.json",
            "agentic/spec/target_literature_search_snapshot.schema.json",
        ),
    ),
    "source_pre_map_policy": (
        "agentic.discovery.literature_acquisition:build_source_routing_pre_map_policy",
        "1.0.0",
        (
            "agentic/discovery/literature_acquisition.py",
            "agentic/discovery/contracts.py",
            "agentic/spec/source_routing_pre_map_policy.schema.json",
        ),
    ),
    "warrant_validation": (
        "agentic.discovery.literature_acquisition:build_source_routing_warrant_validation_packet",
        "1.0.0",
        (
            "agentic/discovery/literature_acquisition.py",
            "agentic/discovery/literature.py",
            "agentic/spec/source_routing_warrant_validation_packet.schema.json",
        ),
    ),
    "claim_mapping": (
        "agentic.discovery.literature:derive_claim_mappings",
        "3.0.0",
        (
            "agentic/discovery/literature.py",
            "agentic/discovery/contracts.py",
            "agentic/spec/theory_object_catalog.schema.json",
            "agentic/spec/literature_semantic_claim_layer.schema.json",
            "agentic/spec/literature_claim_mapping_derivation.schema.json",
            "agentic/spec/literature_claim_mapping_stage_output.schema.json",
        ),
    ),
    "assimilation": (
        "agentic.discovery.literature:assimilate_derived_literature",
        "4.0.0",
        (
            "agentic/discovery/literature.py",
            "agentic/discovery/contracts.py",
            "agentic/spec/literature_assimilation_packet.schema.json",
        ),
    ),
    "source_routing_realization": (
        "agentic.discovery.literature_acquisition:build_source_routing_realization",
        "1.0.0",
        (
            "agentic/discovery/literature_acquisition.py",
            "agentic/discovery/literature.py",
            "agentic/spec/source_routing_realization.schema.json",
        ),
    ),
    "high_risk_input": (
        "agentic.discovery.hypotheses:forge_high_risk_portfolio",
        "2.0.0",
        (
            "agentic/discovery/hypotheses.py",
            "agentic/discovery/literature.py",
            "agentic/spec/high_risk_hypothesis_portfolio.schema.json",
        ),
    ),
    "parent_reflection": (
        "agentic.scripts.run_discovery_operator_protocol:execute[reflective-conceptual-discovery]",
        "1.0.0",
        (
            _OPERATOR_PROTOCOL_PATH,
            _OPERATOR_REGISTRY_PATH,
            "agentic/discovery/workflow.py",
            "agentic/discovery/reflection.py",
            "agentic/spec/reflective_conceptual_discovery_packet.schema.json",
        ),
    ),
    "parent_conceptual_adjudication": (
        "agentic.scripts.run_discovery_operator_protocol:execute[blind-conceptual-preference-adjudicator]",
        "2.0.0",
        (
            _OPERATOR_PROTOCOL_PATH,
            _OPERATOR_REGISTRY_PATH,
            "agentic/discovery/conceptual_adjudication.py",
            "agentic/discovery/semantic_identity.py",
            "agentic/discovery/contracts.py",
            "agentic/spec/conceptual_adjudication.schema.json",
            "agentic/spec/conceptual_adjudication_evidence.schema.json",
        ),
    ),
    "theory_only_synthesis": (
        "agentic.scripts.run_discovery_operator_protocol:execute[reflective-theory-synthesizer]",
        "1.0.0",
        (
            _OPERATOR_PROTOCOL_PATH,
            _OPERATOR_REGISTRY_PATH,
            "agentic/discovery/workflow.py",
            "agentic/discovery/reflection.py",
            "agentic/spec/reflective_conceptual_discovery_packet.schema.json",
        ),
    ),
    "synthesis_conceptual_adjudication": (
        "agentic.scripts.run_discovery_operator_protocol:execute[blind-conceptual-preference-adjudicator]",
        "2.0.0",
        (
            _OPERATOR_PROTOCOL_PATH,
            _OPERATOR_REGISTRY_PATH,
            "agentic/discovery/conceptual_adjudication.py",
            "agentic/discovery/semantic_identity.py",
            "agentic/discovery/contracts.py",
            "agentic/spec/conceptual_adjudication.schema.json",
            "agentic/spec/conceptual_adjudication_evidence.schema.json",
        ),
    ),
}

_THEORY_OBJECTS: tuple[dict[str, Any], ...] = (
    {
        "theory_object_id": "ym-target-scope",
        "object_kind": "concept",
        "label": "Exact four-dimensional Yang-Mills existence and mass-gap target",
        "match_terms": ["yang-mills", "mass gap", "four-dimensional", "continuum"],
        "scope_anchor": True,
    },
    {
        "theory_object_id": "continuum-construction",
        "object_kind": "proof_obligation",
        "label": "Continuum construction and regulator-independent identity",
        "match_terms": [
            "continuum",
            "regulator-independent",
            "continuum limit",
            "constructive field theory",
        ],
        "scope_anchor": False,
    },
    {
        "theory_object_id": "reflection-positivity",
        "object_kind": "mechanism",
        "label": "Reflection positivity and physical reconstruction",
        "match_terms": [
            "reflection-positive",
            "reflection positivity",
            "osterwalder-schrader",
            "reconstruction",
        ],
        "scope_anchor": False,
    },
    {
        "theory_object_id": "spectral-gap",
        "object_kind": "proof_obligation",
        "label": "Positive Hamiltonian spectral gap above the vacuum",
        "match_terms": ["spectral gap", "transfer-operator gap", "mass gap"],
        "scope_anchor": False,
    },
    {
        "theory_object_id": "universality",
        "object_kind": "barrier",
        "label": "Regulator-independent universality and presentation descent",
        "match_terms": [
            "universality",
            "regulator independent",
            "continuum covariance",
        ],
        "scope_anchor": False,
    },
    {
        "theory_object_id": "center-symmetry",
        "object_kind": "mechanism",
        "label": "Center-symmetry and topological mediator",
        "match_terms": [
            "center symmetries",
            "topological field theories",
            "aksz",
            "weil-algebra",
        ],
        "scope_anchor": False,
    },
    {
        "theory_object_id": "correction-lineage",
        "object_kind": "genealogy",
        "label": "Correction, supersession, and retraction lineage",
        "match_terms": ["retracted", "supersedes", "corrects", "corrections", "gap"],
        "scope_anchor": False,
    },
)


class LiteratureProductionChainError(ContractError):
    """A stable failure at the exact-byte-to-theory production boundary."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"literature_production_chain[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise LiteratureProductionChainError(reason_code, message)


def _timestamp(raw: str, *, field: str) -> datetime:
    """Parse one timezone-aware instant and normalize it to UTC."""

    try:
        parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise LiteratureProductionChainError(
            "invalid_timestamp", f"{field} is not an ISO date-time"
        ) from exc
    if parsed.tzinfo is None:
        _fail("invalid_timestamp", f"{field} lacks an explicit timezone")
    return parsed.astimezone(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_relative_path(raw: str) -> PurePosixPath:
    """Accept only canonical POSIX child paths for descriptor-anchored reads."""

    path = PurePosixPath(raw)
    if (
        not raw
        or "\\" in raw
        or path.is_absolute()
        or path.as_posix() != raw
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        _fail("unsafe_relative_path", f"unsafe authority path: {raw!r}")
    return path


def _read_exact_regular_file(root: Path, relative: str) -> bytes:
    """Read one root-anchored regular file without following any link edge.

    The open descriptor is the authority: identity is checked before and after
    the read, and the named entry is reopened by directory file descriptor.
    This prevents a JSON-equivalent replacement, symlink, hardlink, or path
    traversal from becoming an unnoticed source or dependency substitution.
    """

    path = _safe_relative_path(relative)
    resolved_root = root.resolve(strict=True)
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
            _fail("artifact_not_regular", f"artifact is not a regular file: {relative}")
        if before.st_nlink != 1:
            _fail("artifact_hardlink", f"artifact has multiple hard links: {relative}")
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
            _fail("artifact_changed_during_read", f"artifact changed while read: {relative}")
        return b"".join(chunks)
    except LiteratureProductionChainError:
        raise
    except OSError as exc:
        raise LiteratureProductionChainError(
            "artifact_unreadable", f"cannot read {relative}: {exc}"
        ) from exc
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _load_json_bytes(data: bytes, *, relative: str) -> dict[str, Any]:
    try:
        payload = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LiteratureProductionChainError(
            "artifact_json_invalid", f"cannot decode {relative}: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        _fail("artifact_not_object", f"JSON artifact is not an object: {relative}")
    return payload


def _file_identity(
    *,
    role: str,
    relative_path: str,
    data: bytes,
    content_digest: str | None = None,
) -> dict[str, Any]:
    return {
        "role": role,
        "relative_path": relative_path,
        "sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "content_digest": content_digest,
    }


def _code_file_identity(code_root: Path, relative: str, *, role: str) -> dict[str, Any]:
    data = _read_exact_regular_file(code_root, relative)
    return _file_identity(
        role=role,
        relative_path=relative,
        data=data,
        content_digest=None,
    )


def _implementation(stage_id: str, code_root: Path) -> dict[str, Any]:
    """Bind one stage to exact implementation and dependency file bytes."""

    symbol, version, dependency_paths = _STAGE_IMPLEMENTATIONS[stage_id]
    primary_path = dependency_paths[0]
    code_artifact = _code_file_identity(
        code_root, primary_path, role=f"{stage_id}:implementation"
    )
    ordered_paths = list(dict.fromkeys((_MODULE_PATH, *dependency_paths[1:])))
    dependencies = [
        _code_file_identity(code_root, path, role=f"{stage_id}:dependency")
        for path in ordered_paths
    ]
    dependency_set_digest = canonical_digest(dependencies)
    implementation = {
        "symbol": symbol,
        "implementation_version": version,
        "code_artifact": code_artifact,
        "dependencies": dependencies,
        "dependency_set_digest": dependency_set_digest,
    }
    implementation["implementation_digest"] = canonical_digest(implementation)
    return implementation


def _binding(
    role: str,
    digest: str,
    *,
    source_stage_id: str | None = None,
    source_artifact_path: str | None = None,
) -> dict[str, Any]:
    return {
        "role": role,
        "digest": digest,
        "source_stage_id": source_stage_id,
        "source_artifact_path": source_artifact_path,
    }


def _derived_intermediate(
    role: str,
    value: Sequence[Mapping[str, Any]],
    *,
    derived_from_input_roles: Sequence[str],
) -> dict[str, Any]:
    """Type a deterministic stage-local projection without granting authority.

    These rows describe values computed *inside* an adjudication stage from its
    already bound proposal packet.  They are intentionally disjoint from
    ``request.input_bindings``: listing them as request inputs would
    retrospectively promote a derived representation into upstream authority.
    """

    rows = [copy.deepcopy(dict(row)) for row in value]
    return {
        "role": role,
        "derivation_kind": "stage_internal_deterministic_projection",
        "derived_from_input_roles": list(derived_from_input_roles),
        "row_count": len(rows),
        "content_digest": canonical_digest(rows),
        "authority_class": "derived_non_authoritative_intermediate",
        "authority_boundary": (
            "Digest and cardinality describe a deterministic stage-local "
            "representation only; the rows are not upstream evidence, caller "
            "authority, independent review, or an external conceptual judgment."
        ),
    }


def _stage_record(
    *,
    stage_index: int,
    stage_id: str,
    identity: Mapping[str, Any],
    implementation: Mapping[str, Any],
    input_bindings: Sequence[Mapping[str, Any]],
    output_role: str,
    output_payload: Mapping[str, Any],
    output_schema: str | None,
    started_at: str,
    completed_at: str,
    status: str = "succeeded",
    producer_authority: str = "local_unregistered_execution",
    reason_codes: Sequence[str] = (),
    authority_boundary: str,
    native_receipt: Mapping[str, Any] | None = None,
    derived_intermediates: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Seal one request, output, and receipt without circular identifiers."""

    bindings = [copy.deepcopy(dict(row)) for row in input_bindings]
    input_digest = canonical_digest(bindings)
    request_id = stable_identifier(
        "production-request",
        stage_id,
        identity,
        input_digest,
        implementation["implementation_digest"],
        started_at,
    )
    request = {
        "request_id": request_id,
        "stage_id": stage_id,
        "target_id": identity["target_id"],
        "run_id": identity["run_id"],
        "state_version": identity["state_version"],
        "created_at": started_at,
        "publication_enabled": False,
        "world_commissioning_requested": False,
        "input_bindings": bindings,
        "input_digest": input_digest,
        "implementation_digest": implementation["implementation_digest"],
        "dependency_set_digest": implementation["dependency_set_digest"],
    }
    request["request_digest"] = canonical_digest(request)
    payload = copy.deepcopy(dict(output_payload))
    output_digest = canonical_digest(payload)
    receipt_id = stable_identifier(
        "production-receipt",
        request["request_digest"],
        status,
        output_digest,
        completed_at,
    )
    receipt = {
        "receipt_id": receipt_id,
        "status": status,
        "started_at": started_at,
        "completed_at": completed_at,
        "request_id": request_id,
        "request_digest": request["request_digest"],
        "input_digest": input_digest,
        "output_digest": output_digest,
        "implementation_digest": implementation["implementation_digest"],
        "dependency_set_digest": implementation["dependency_set_digest"],
        "producer_authority": producer_authority,
        "reason_codes": sorted(set(str(row) for row in reason_codes)),
        "authority_boundary": authority_boundary,
        "native_receipt": (
            copy.deepcopy(dict(native_receipt))
            if native_receipt is not None
            else None
        ),
    }
    return {
        "stage_index": stage_index,
        "stage_id": stage_id,
        "status": status,
        "request": request,
        "receipt": receipt,
        "implementation": copy.deepcopy(dict(implementation)),
        "derived_intermediates": [
            copy.deepcopy(dict(row)) for row in derived_intermediates
        ],
        "output": {
            "artifact_role": output_role,
            "schema_path": output_schema,
            "content_digest": output_digest,
            "payload": payload,
        },
    }


def _load_source_bundle(
    authority_root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Load and cross-validate the exact eight checked-in source artifacts."""

    root = authority_root.resolve(strict=True)
    capture_bytes = _read_exact_regular_file(root, CAPTURE_NAME)
    acquisition_bytes = _read_exact_regular_file(root, ACQUISITION_NAME)
    capture = _load_json_bytes(capture_bytes, relative=CAPTURE_NAME)
    acquisition = _load_json_bytes(acquisition_bytes, relative=ACQUISITION_NAME)
    if capture.get("target_id") != TARGET_ID or acquisition.get("target_id") != TARGET_ID:
        _fail("target_mismatch", "the exact source bundle names another target")

    artifacts_by_path: dict[str, tuple[dict[str, Any], bytes]] = {}
    source_artifacts = [
        _file_identity(
            role="capture",
            relative_path=CAPTURE_NAME,
            data=capture_bytes,
            content_digest=str(capture.get("content_digest") or "") or None,
        ),
        _file_identity(
            role="normalized_acquisition",
            relative_path=ACQUISITION_NAME,
            data=acquisition_bytes,
            content_digest=str(acquisition.get("content_digest") or "") or None,
        ),
    ]
    for descriptor in capture.get("provider_response_artifacts", []):
        relative = str(descriptor.get("path") or "")
        _safe_relative_path(relative)
        payload, data = load_tool_response_artifact(root / relative, authority_root=root)
        artifacts_by_path[relative] = (payload, data)
        source_artifacts.append(
            _file_identity(
                role=f"tool_response:{payload['lane_type']}",
                relative_path=relative,
                data=data,
                content_digest=str(payload["content_digest"]),
            )
        )
    authority = validate_capture_acquisition_bundle(
        capture=capture,
        acquisition=acquisition,
        artifacts_by_path=artifacts_by_path,
        version_graphs=capture.get("version_lineages", []),
    )
    if len(source_artifacts) != 8:
        _fail("source_artifact_count", "exactly eight source artifacts are required")
    embedded_graphs = [
        {
            "json_pointer": f"/version_lineages/{index}",
            "graph_id": str(graph["graph_id"]),
            "content_digest": str(graph["content_digest"]),
        }
        for index, graph in enumerate(capture["version_lineages"])
    ]
    source_bundle = {
        "authority_root_kind": "caller_supplied_immutable_bundle_root",
        "capture_id": str(capture["capture_id"]),
        "snapshot_id": str(acquisition["snapshot_id"]),
        "artifacts": source_artifacts,
        "embedded_version_graphs": embedded_graphs,
        "source_ids": list(authority["source_ids"]),
        "authority_boundary": str(authority["authority_boundary"]),
    }
    source_bundle["bundle_digest"] = canonical_digest(source_bundle)
    return capture, acquisition, authority, source_bundle


def _theory_catalog(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Freeze the exact YM burdens used by the deterministic claim mapper."""

    return build_theory_object_catalog(
        target_id=TARGET_ID,
        theory_state_digest=str(snapshot["theory_state_digest"]),
        theory_objects=copy.deepcopy(_THEORY_OBJECTS),
    )


def _algorithm_contracts(
    implementations: Mapping[str, Mapping[str, Any]],
    theory_catalog: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Bind pre-map algorithms before any warrant or mapping output exists."""

    rows = []
    settings = {
        "warrant_validation": {
            "policy": "exact snapshot-enclosed semantic warrants only",
        },
        "claim_mapping": {
            "mapping_algorithm": CLAIM_MAPPING_ALGORITHM_ID,
            "theory_catalog_digest": theory_catalog["content_digest"],
        },
        "assimilation": {
            "mapping_mode": "deterministic_claim_derivation",
            "theory_catalog_digest": theory_catalog["content_digest"],
            "freshness_max_age_seconds": FRESHNESS_MAX_AGE_SECONDS,
        },
    }
    for stage in ("warrant_validation", "claim_mapping", "assimilation"):
        implementation = implementations[stage]
        rows.append(
            {
                "stage": stage,
                "component_id": str(implementation["symbol"]),
                "algorithm_id": (
                    CLAIM_MAPPING_ALGORITHM_ID
                    if stage == "claim_mapping"
                    else f"ym22-{stage}-deterministic.v1"
                ),
                "config_id": f"ym22-literature-production-{stage}.v1",
                "config_digest": canonical_digest(settings[stage]),
                "authority_class": "local_unregistered_code_identity",
            }
        )
    return rows


def _high_risk_charter(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """State the exact physics target and drift boundary for authored fallback seeds."""

    return {
        "target_id": TARGET_ID,
        "target_statement": (
            "Construct and understand a nontrivial four-dimensional Yang-Mills "
            "theory satisfying the exact existence and mass-gap target without "
            "replacing continuum or physical requirements by finite proxies."
        ),
        "theory_state_digest": snapshot["theory_state_digest"],
        "root_tensions": [
            "Finite or regulated coercive control does not itself provide regulator-independent continuum identity.",
            "Euclidean decay estimates do not themselves identify a complete physical nonvacuum spectrum.",
            "Local constructive presentations do not themselves prove coherent regulator-independent equivalence.",
        ],
        "target_commitments": [
            "Preserve four-dimensional continuum construction, nontriviality, Osterwalder-Schrader reconstruction, and a positive physical mass gap above the vacuum."
        ],
        "protected_successes": [
            "Preserve exact finite and regulated estimates only within their proved scope.",
            "Preserve correction and supersession lineages rather than treating earlier versions as current.",
        ],
        "forbidden_target_drift": (
            "No finite-volume, lattice-only, toy-model, bibliography-only, or "
            "conceptual-language proxy may be reported as the continuum Yang-Mills result."
        ),
    }


def _reflection_request(
    *,
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    operator_receipt_ids: Sequence[str],
) -> dict[str, Any]:
    """Translate the executed literature outputs into the existing parent contract."""

    return {
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "branch_id": "root",
        "state_version": STATE_VERSION,
        "prior_conceptual_state_ref": "state:0",
        "discovery_charter": {
            "essential_question": (
                "Which conceptual structure can join continuum construction, "
                "physical spectral detection, and regulator-independent identity "
                "without collapsing their distinct burdens?"
            ),
            "desired_understanding": (
                "Explain why finite coercivity, Euclidean reconstruction, and "
                "universality repeatedly fail to close one another, and expose "
                "the minimal mediators needed between them."
            ),
            "bottleneck_diagnosis": "conceptual",
            "bottleneck_evidence": (
                "The exact capture separates correction-aware proof claims, "
                "constructive-field-theory genealogy, center-symmetry mechanisms, "
                "and direct continuum challenges without validating a bridge among them."
            ),
            "target_commitments": list(_high_risk_charter(snapshot)["target_commitments"]),
            "relevance_horizon": (
                "A successful conceptual mediation must reorganize exact continuum, "
                "reconstruction, and spectral-gap obligations before any support experiment."
            ),
            "incumbent_framework": (
                "regulated coercivity followed by reconstruction and universality transfer"
            ),
            "conceptual_opacity": (
                "Scale production, observable completeness, and presentation descent "
                "are tracked as adjacent burdens rather than one typed explanatory architecture."
            ),
            "non_claim_boundary": (
                "This diagnostic reflection establishes no novelty, theorem, continuum "
                "construction, mass gap, source truth, or literature benefit."
            ),
        },
        "conceptual_genealogy": {
            "inherited_concepts": [
                "regulated coercivity",
                "reflection positivity",
                "Osterwalder-Schrader reconstruction",
                "spectral gap",
                "universality",
                "center symmetry",
            ],
            "historical_or_logical_formation": [
                "Constructive field theory separated regulated control from continuum reconstruction.",
                "Correction lineages expose architecture changes that metadata alone cannot validate.",
            ],
            "protected_successes": list(_high_risk_charter(snapshot)["protected_successes"]),
            "rejected_or_retired_ancestors": [
                "finite certificate as continuum proof",
                "uncorrected predecessor as current authority",
            ],
            "hidden_assumptions": [
                "a positive regulated scale transports automatically to a complete physical spectrum",
                "different regulator presentations descend automatically to one theory",
            ],
        },
        "literature_basis": {
            "selected_snapshot_id": snapshot["snapshot_id"],
            "snapshot_target_id": TARGET_ID,
            "selected_snapshot_digest": snapshot["content_digest"],
            "search_completed_utc": snapshot["search_completed_at"],
            "freshness_status": assimilation["resolution"]["freshness_status"],
            "search_receipt_ids": [
                *[row["receipt_id"] for row in snapshot["validator_receipts"]],
                *[row["lane_id"] for row in snapshot["lane_receipts"]],
            ],
            "assimilation_packet_ref": (
                f"manifest-stage:{ORDERED_STAGE_IDS.index('assimilation')}"
            ),
            "source_to_theory_delta_summary": [
                f"{len(assimilation['theory_mappings'])} claim-level mappings were "
                "deterministically routed as unresolved, correction-aware reframe, "
                "retire, or justified-no-change events."
            ],
            "literature_generated_questions": [
                "What mediator separates regulated scale production from physical observable completeness?",
                "What coherence object distinguishes presentation equivalence from merely parallel regulator limits?",
                "Which correction-sensitive premise changes survive the v1-v2-v3 architecture lineage?",
            ],
            "coverage_limitations": list(snapshot["coverage_limits"]),
            "superseded_snapshot_ids": [],
        },
        "root_tensions": [
            {
                "tension_id": "ym-continuum-spectrum-presentation",
                "opposed_commitments": [
                    "regulated constructive control",
                    "physical continuum identity and spectrum",
                ],
                "strongest_form_of_each_side": [
                    "Finite or regulated estimates can be exact within their declared carrier.",
                    "The target requires a nontrivial regulator-independent continuum theory with a positive physical gap.",
                ],
                "minimal_incompatibility_or_missing_mediation": (
                    "No validated mediator currently transports a regulated scale "
                    "through observable completeness and coherent presentation descent."
                ),
                "regime": "pure four-dimensional Yang-Mills across admissible regulators",
                "why_root_level": (
                    "Without this mediation, improving a local estimate cannot "
                    "determine whether the exact target burden changed."
                ),
            }
        ],
        "high_risk_portfolio": copy.deepcopy(dict(portfolio)),
        "operator_receipt_ids": list(operator_receipt_ids),
        "explicit_unknowns": [
            "Whether any proposed mediator admits nontrivial continuum mathematics.",
            "Whether the bounded source metadata correctly represents the underlying works.",
        ],
    }


def _operator_request(stage: str) -> dict[str, Any]:
    return {
        "identity": {
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "branch_id": "root",
            "state_version": STATE_VERSION,
        },
        "parameters": {"stage": stage},
    }


def _execute_reflective_operator(
    *,
    operator_id: str,
    stage: str,
    envelope: Mapping[str, Any],
    created_at: str,
    code_root: Path,
) -> dict[str, Any]:
    """Run the existing in-process operator with an injected replay clock."""

    with patch("agentic.discovery.workflow.utc_now", return_value=created_at):
        packet, _unknowns = execute_operator(
            operator_id,
            _operator_request(stage),
            envelope,
            code_root / ".unused-publication-disabled-output.json",
            code_root,
        )
    validate_packet_invariants(packet)
    return packet


_DIMENSION_WARRANT_PATHS = {
    "essential_relevance": "/target_pressures_addressed",
    "explanatory_mediation": "/mechanism_or_principle",
    "conceptual_depth": "/primitives",
    "unification_power": "/unification_claims/mappings",
    "preserved_difference": "/unification_claims/preserved_differences",
    "generativity": "/formalization_seeds",
    "reflective_resilience": "/correction_conditions",
    "truth_aptness": "/residual_contradictions",
}

_DEEP_LENS_LANGUAGE = {
    "ontological": {
        "question": (
            "Which candidate primitive has explanatory reality rather than merely "
            "renaming the unresolved Yang--Mills burden?"
        ),
        "tension": (
            "The mediator must be a real explanatory commitment while remaining "
            "corrigible by a logically distinct target boundary."
        ),
        "assumption": (
            "The inherited view assumes that naming an abstract carrier is enough "
            "to establish an ontologically load-bearing mediator."
        ),
        "analysis": (
            "The candidate is tested through its exact mechanism and typed mediator, "
            "with the residual contradiction retained as an independent failure carrier."
        ),
        "consequence_kind": "relation_revised",
        "consequence": (
            "Keep the proposed mediator provisional until removing it changes a "
            "target-level explanatory dependency."
        ),
        "physics_question": (
            "Which independently specified carrier would change the continuum "
            "construction programme if it were removed?"
        ),
    },
    "dialectical": {
        "question": (
            "Which opposition is mediated without collapsing the target burden "
            "into its own correction condition?"
        ),
        "tension": (
            "The target pressure and correction boundary jointly resist premature "
            "closure, yet neither can be identified with the other."
        ),
        "assumption": (
            "The inherited frame assumes that every correction condition merely "
            "restates the original theoretical burden."
        ),
        "analysis": (
            "The candidate registers pressure and correction as distinct source "
            "cases connected by a mediator that either side can defeat."
        ),
        "consequence_kind": "tension_registered",
        "consequence": (
            "Preserve the opposition as an explicit constraint on every proposed "
            "bridge between construction and physical interpretation."
        ),
        "physics_question": (
            "Which countermodel separates genuine mediation from a verbal compromise "
            "between the two source cases?"
        ),
    },
    "explanatory": {
        "question": (
            "Which directed dependency increases target understanding instead of "
            "adding a second descriptive vocabulary?"
        ),
        "tension": (
            "The graph must add a dependency while preserving the correction path "
            "that can still defeat the proposed mechanism."
        ),
        "assumption": (
            "The inherited explanation treats a shared abstract label as sufficient "
            "unification across distinct constructive and spectral burdens."
        ),
        "analysis": (
            "The candidate adds typed arrows from pressure and failure boundary to "
            "the mediator, making their direction and defeat conditions inspectable."
        ),
        "consequence_kind": "mechanism_revised",
        "consequence": (
            "Retain only explanatory dependencies whose removal changes a concrete "
            "Yang--Mills theory question."
        ),
        "physics_question": (
            "Which removal test shows that the explanatory graph materially changes "
            "the next physics-facing formalization obligation?"
        ),
    },
}


def _typed_adjudication_system(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Compile one reflected candidate into the existing typed graph contract."""

    system = copy.deepcopy(dict(raw))
    primitive = str(system["primitives"][0])
    relation = str(system["relations_operations_and_dynamics"][0])
    mechanism = str(system["mechanism_or_principle"])
    before_graph = {
        "nodes": [
            {
                "node_id": "target-pressure-case",
                "node_kind": "source_case",
                "label": "Exact target pressure carried by this candidate",
                "content_paths": ["/target_pressures_addressed/0"],
            },
            {
                "node_id": "correction-boundary-case",
                "node_kind": "source_case",
                "label": "Residual correction boundary carried by this candidate",
                "content_paths": ["/residual_contradictions/0"],
            },
        ],
        "edges": [],
    }
    added_nodes = [
        {
            "node_id": "candidate-mediator",
            "node_kind": "mediator",
            "label": "Provisional target-specific explanatory mediator",
            "content_paths": [
                "/mechanism_or_principle",
                "/unification_claims/mediator/statement",
            ],
        }
    ]
    added_edges = [
        {
            "edge_id": "pressure-to-mediator",
            "source_node_id": "target-pressure-case",
            "relation_kind": "mediates",
            "target_node_id": "candidate-mediator",
            "statement": (
                "The candidate mechanism mediates the explicit target pressure "
                "without declaring that pressure solved."
            ),
            "warrant_paths": ["/mechanism_or_principle"],
        },
        {
            "edge_id": "boundary-to-mediator",
            "source_node_id": "correction-boundary-case",
            "relation_kind": "constrains",
            "target_node_id": "candidate-mediator",
            "statement": (
                "The residual contradiction constrains the mediator and remains "
                "a live route for correction or rejection."
            ),
            "warrant_paths": ["/residual_contradictions/0"],
        },
    ]
    after_graph = {
        "nodes": [*before_graph["nodes"], *added_nodes],
        "edges": added_edges,
    }
    system["unification_claims"] = {
        "unification_kind": "regime_indexed_mediation",
        "source_case_ids": [
            "target-pressure-case",
            "correction-boundary-case",
        ],
        "mediator": {
            "statement": (
                "The proposed mechanism mediates one target pressure under an "
                "independent correction boundary while preserving their logical "
                f"difference: {mechanism}"
            ),
            "primitive_refs": [
                f"Candidate primitive carrier anchored by {primitive}"
            ],
            "relation_refs": [
                f"Candidate relation carrier anchored by {relation}"
            ],
            "node_ids": ["candidate-mediator"],
        },
        "mappings": [
            {
                "mapping_id": "target-pressure-map",
                "source_case_id": "target-pressure-case",
                "target_node_id": "candidate-mediator",
                "map_kind": "mediation",
                "bridge_statement": (
                    "The exact target pressure enters as a burden to explain, "
                    "not as a conclusion already assumed by the mediator."
                ),
                "warrant_paths": [
                    "/target_pressures_addressed/0",
                    "/mechanism_or_principle",
                ],
            },
            {
                "mapping_id": "correction-boundary-map",
                "source_case_id": "correction-boundary-case",
                "target_node_id": "candidate-mediator",
                "map_kind": "comparison",
                "bridge_statement": (
                    "The residual contradiction enters as a correction boundary "
                    "that can defeat the proposed mediation."
                ),
                "warrant_paths": [
                    "/residual_contradictions/0",
                    "/correction_conditions/0",
                ],
            },
        ],
        "preserved_differences": [
            {
                "difference_id": "pressure-not-correction",
                "source_case_ids": ["target-pressure-case"],
                "statement": (
                    "The target pressure names what needs explanation and is not "
                    "identical to the condition that corrects that explanation."
                ),
                "preservation_witness_paths": [
                    "/target_pressures_addressed/0",
                    "/identities_and_differences/0",
                ],
                "witness_node_ids": [
                    "target-pressure-case",
                    "candidate-mediator",
                ],
                "witness_edge_ids": ["pressure-to-mediator"],
            },
            {
                "difference_id": "correction-not-pressure",
                "source_case_ids": ["correction-boundary-case"],
                "statement": (
                    "The correction boundary can reject the mediator without "
                    "changing the original target burden or proving its negation."
                ),
                "preservation_witness_paths": [
                    "/correction_conditions/0",
                    "/residual_contradictions/0",
                ],
                "witness_node_ids": [
                    "correction-boundary-case",
                    "candidate-mediator",
                ],
                "witness_edge_ids": ["boundary-to-mediator"],
            },
        ],
        "explanatory_graph_transition": {
            "before_graph": before_graph,
            "after_graph": after_graph,
            "before_graph_digest": canonical_digest(before_graph),
            "after_graph_digest": canonical_digest(after_graph),
            "added_nodes": added_nodes,
            "added_edges": added_edges,
            "new_explanatory_dependencies": [
                "The target burden is linked to a provisional mediator whose "
                "residual contradiction supplies an independent correction boundary."
            ],
        },
        "scope_conditions": [
            "This mediation applies only to the exact Yang--Mills target pressure "
            "recorded by the parent reflection."
        ],
        "transfer_obligations": [
            "Show that the mediator transports the target burden without "
            "presupposing a continuum theory or positive physical gap."
        ],
        "erasure_risks": [
            "A generic mediator vocabulary could erase the distinction between "
            "an explanatory burden and its correction condition."
        ],
        "failure_conditions": [
            "Demote the candidate when its correction boundary is definitionally "
            "equivalent to the target conclusion or cannot alter the programme."
        ],
    }
    return system


def _pointer_value(payload: Mapping[str, Any], path: str) -> Any:
    current: Any = payload
    for token in path.lstrip("/").split("/"):
        current = current[token]
    return current


def _relevant_round_count(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> int:
    alias = str(candidate["candidate_alias"])
    content = candidate["content"]
    inherited = {
        str(value)
        for value in content.get("conceptual_ancestors", [])
        if str(value).startswith("candidate-")
    }
    aliases = {alias, *inherited}
    return sum(
        bool(aliases & set(row.get("content", {}).get("system_ids", [])))
        for row in packet.get("reflection_rounds", [])
    )


def _dimension_ratings(
    candidate: Mapping[str, Any], packet: Mapping[str, Any], lens: str
) -> dict[str, str]:
    content = candidate["content"]
    mechanism_words = len(str(content["mechanism_or_principle"]).split())
    primitives = len(content["primitives"])
    relations = len(content["relations_operations_and_dynamics"])
    pressures = len(content["target_pressures_addressed"])
    questions = len(content["implications_and_new_questions"])
    seeds = len(content["formalization_seeds"])
    corrections = len(content["correction_conditions"])
    contradictions = len(content["residual_contradictions"])
    mappings = len(content["unification_claims"]["mappings"])
    differences = len(content["unification_claims"]["preserved_differences"])
    relevant_rounds = _relevant_round_count(candidate, packet)
    adequate = {
        "essential_relevance": pressures >= 1,
        "explanatory_mediation": mechanism_words >= 9 and relations >= 1,
        "conceptual_depth": primitives >= 2 or mechanism_words >= 14,
        "unification_power": mappings >= 2,
        "preserved_difference": differences >= 2,
        "generativity": questions >= 1 and seeds >= 1,
        "reflective_resilience": corrections >= 1 and bool(packet["reflection_rounds"]),
        "truth_aptness": corrections >= 1 and contradictions >= 1,
    }
    strong_by_lens = {
        "ontological": {
            "essential_relevance": pressures >= 2,
            "explanatory_mediation": mechanism_words >= 20 and relations >= 2,
            "conceptual_depth": primitives >= 4,
            "unification_power": mappings >= 2 and primitives >= 4,
            "preserved_difference": differences >= 2 and primitives >= 3,
            "generativity": questions >= 3 and seeds >= 3,
            "reflective_resilience": relevant_rounds >= 1 and corrections >= 2,
            "truth_aptness": corrections >= 3 and contradictions >= 1,
        },
        "dialectical": {
            "essential_relevance": pressures >= 2,
            "explanatory_mediation": mechanism_words >= 16 and contradictions >= 1,
            "conceptual_depth": primitives >= 3 and contradictions >= 1,
            "unification_power": mappings >= 2 and relevant_rounds >= 1,
            "preserved_difference": differences >= 2 and contradictions >= 1,
            "generativity": questions >= 2 and seeds >= 2,
            "reflective_resilience": relevant_rounds >= 1 and corrections >= 2,
            "truth_aptness": corrections >= 2 and contradictions >= 1,
        },
        "explanatory": {
            "essential_relevance": pressures >= 2,
            "explanatory_mediation": mechanism_words >= 20 and relations >= 2,
            "conceptual_depth": primitives >= 3 and relations >= 2,
            "unification_power": mappings >= 2 and mechanism_words >= 18,
            "preserved_difference": differences >= 2 and relations >= 2,
            "generativity": questions >= 2 and seeds >= 2,
            "reflective_resilience": relevant_rounds >= 1 and corrections >= 2,
            "truth_aptness": corrections >= 2 and contradictions >= 1,
        },
    }[lens]
    return {
        dimension: (
            "strong"
            if strong_by_lens[dimension]
            else "adequate"
            if adequate[dimension]
            else "weak"
        )
        for dimension in DIMENSIONS
    }


def _deep_lens_judgment(
    candidate: Mapping[str, Any], packet: Mapping[str, Any], lens: str
) -> dict[str, Any]:
    content = candidate["content"]
    ratings = _dimension_ratings(candidate, packet, lens)
    findings = {}
    for dimension in DIMENSIONS:
        path = _DIMENSION_WARRANT_PATHS[dimension]
        findings[dimension] = {
            "rating": ratings[dimension],
            "warrants": [
                {
                    "path": path,
                    "value_digest": canonical_digest(_pointer_value(content, path)),
                    "explanation": (
                        "This exact candidate surface bears the named "
                        "noncompensatory conceptual dimension under this lens."
                    ),
                }
            ],
            "strongest_objection": (
                "The apparent strength may remain decorative unless the cited "
                "content changes an independently correctable target dependency."
            ),
            "correction_test": (
                "Remove or countermodel the cited content and demote the rating "
                "unless a target-relevant explanatory loss follows."
            ),
        }
    language = _DEEP_LENS_LANGUAGE[lens]
    warrant_paths = [
        "/mechanism_or_principle",
        "/unification_claims/mediator/statement",
    ]
    lens_warrants = [
        {
            "path": path,
            "value_digest": canonical_digest(_pointer_value(content, path)),
            "explanation": (
                "This exact content identifies the mechanism and typed mediator "
                "examined by the declared deep lens."
            ),
        }
        for path in warrant_paths
    ]
    return {
        "dimensions": findings,
        "deep_lens_analysis": {
            "lens_family": lens,
            "focal_question": language["question"],
            "content_warrants": lens_warrants,
            "root_aporia_or_tension": language["tension"],
            "inherited_assumption_exposed": language["assumption"],
            "candidate_specific_analysis": (
                f"{language['analysis']} The candidate mediator is: "
                f"{content['unification_claims']['mediator']['statement']}"
            ),
            "conceptual_consequence": {
                "kind": language["consequence_kind"],
                "changed_paths": ["/mechanism_or_principle"],
                "statement": language["consequence"],
            },
            "physics_value_handback": {
                "target_pressure_paths": ["/target_pressures_addressed/0"],
                "changed_theory_question": language["physics_question"],
                "relevance_limit": (
                    "This internal analysis redirects theory work only; it "
                    "establishes no source truth, theorem, physical equivalence, "
                    "external merit, or Yang--Mills mass gap."
                ),
            },
            "strongest_objection": (
                "The proposed mediator may remain decorative unless its typed "
                "dependency survives a countermodel and removal test."
            ),
            "correction_test": (
                "Remove the mediator and demote this analysis unless a "
                "target-relevant explanatory dependency is thereby lost."
            ),
        },
    }


def _ontological_adjudication_judge(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _deep_lens_judgment(candidate, packet, "ontological")


def _dialectical_adjudication_judge(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _deep_lens_judgment(candidate, packet, "dialectical")


def _explanatory_adjudication_judge(
    candidate: Mapping[str, Any], packet: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _deep_lens_judgment(candidate, packet, "explanatory")


_ADJUDICATION_JUDGES = (
    ("ym22-ontological-critic", "ontological", _ontological_adjudication_judge),
    ("ym22-dialectical-critic", "dialectical", _dialectical_adjudication_judge),
    ("ym22-explanatory-critic", "explanatory", _explanatory_adjudication_judge),
)


def _execute_conceptual_adjudication(
    *,
    stage_id: str,
    proposal_packet: Mapping[str, Any],
    proposal_receipt_ids: Sequence[str],
    snapshot: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    proposer_identity: str,
    previous_evidence: Mapping[str, Any] | None,
    created_at: str,
    code_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Execute the registered adjudicator with an honest correlated panel."""

    systems = [
        _typed_adjudication_system(row)
        for row in proposal_packet["conceptual_systems"]
    ]
    rounds = copy.deepcopy(list(proposal_packet["reflection_rounds"]))
    frozen_genealogy: list[dict[str, Any]] = []
    source_bindings = build_adjudication_source_bindings(
        run_id=RUN_ID,
        state_version=STATE_VERSION,
        theory_state_digest=str(snapshot["theory_state_digest"]),
        literature_snapshot_digest=str(snapshot["content_digest"]),
        high_risk_portfolio_digest=str(portfolio["content_digest"]),
        systems=systems,
        reflection_rounds=rounds,
        frozen_genealogy=frozen_genealogy,
        proposer_receipt_ids=proposal_receipt_ids,
    )
    root_tensions = [
        str(row["minimal_incompatibility_or_missing_mediation"])
        for row in proposal_packet["root_tensions"]
    ]
    blind_packet, candidate_bindings = build_blind_packet(
        target_id=TARGET_ID,
        stage_id=stage_id,
        target_charter={"root_tensions": root_tensions},
        systems=systems,
        reflection_rounds=rounds,
        proposer_identity=proposer_identity,
        source_bindings=source_bindings,
        counterbalance_seed=f"ym22-production-{stage_id}",
    )
    reports = [
        build_judge_report(
            blind_packet,
            adjudicator_id=judge_id,
            perspective=lens,
            version="ym22-local-correlated-panel/1.0.0",
            judge=judge,
            created_at=created_at,
            independence_claim="correlated_internal",
            lens_family=lens,
        )
        for judge_id, lens, judge in _ADJUDICATION_JUDGES
    ]
    envelope = {
        "blind_packet": blind_packet,
        "judge_reports": reports,
        "systems": systems,
        "reflection_rounds": rounds,
        "frozen_genealogy": frozen_genealogy,
        "candidate_bindings": candidate_bindings,
        "theory_state_digest": snapshot["theory_state_digest"],
        "literature_snapshot_digest": snapshot["content_digest"],
        "high_risk_portfolio_digest": portfolio["content_digest"],
        "proposer_receipt_ids": list(proposal_receipt_ids),
        "previous_evidence": (
            None if previous_evidence is None else copy.deepcopy(dict(previous_evidence))
        ),
        "previous_evidence_digest": (
            None if previous_evidence is None else previous_evidence["evidence_digest"]
        ),
        "created_at": created_at,
    }
    evidence, _unknowns = execute_operator(
        "blind-conceptual-preference-adjudicator",
        _operator_request(stage_id),
        envelope,
        code_root / ".unused-publication-disabled-output.json",
        code_root,
    )
    authority = evidence["content_adjudication"]["authority"]
    if (
        authority["plural_independent_perspectives"] is not False
        or authority["panel_evidence_class"] != "correlated_internal_critique"
        or authority["external_human_evidence_available"] is not False
        or authority["external_generalization_authorized"] is not False
    ):
        _fail(
            "adjudication_authority_overclaim",
            "local adjudication escaped its correlated, non-external authority boundary",
        )
    return evidence, systems


def _native_source_receipts(
    *,
    policy: Mapping[str, Any],
    requirements: Sequence[Mapping[str, Any]],
    identity: Mapping[str, Any],
    start: datetime,
) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for index, requirement in enumerate(requirements):
        started_at = _iso(start + timedelta(seconds=1 + 2 * index))
        completed_at = _iso(start + timedelta(seconds=2 + 2 * index))
        receipts.append(
            {
                "receipt_id": stable_identifier(
                    "source-stage-receipt",
                    requirement["stage"],
                    policy["policy_digest"],
                    requirement["input_digest"],
                    requirement["output_digest"],
                ),
                "stage": requirement["stage"],
                "status": "succeeded",
                "identity": copy.deepcopy(dict(identity)),
                "pre_map_policy_id": policy["policy_id"],
                "pre_map_policy_digest": policy["policy_digest"],
                "algorithm_contract_digest": requirement[
                    "algorithm_contract_digest"
                ],
                "started_at": started_at,
                "completed_at": completed_at,
                "input_digest": requirement["input_digest"],
                "output_digest": requirement["output_digest"],
            }
        )
    return receipts


def _manifest_without_digest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(dict(manifest))
    payload.pop("manifest_digest", None)
    return payload


def _build_manifest(
    *,
    authority_root: Path,
    code_root: Path,
    execution_started_at: str | None,
) -> dict[str, Any]:
    capture, snapshot, acquisition_authority, source_bundle = _load_source_bundle(
        authority_root
    )
    validate_snapshot(snapshot)
    identity = {
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "state_version": STATE_VERSION,
    }
    search_completed = _timestamp(
        str(snapshot["search_completed_at"]), field="snapshot search completion"
    )
    start = (
        search_completed + timedelta(seconds=1)
        if execution_started_at is None
        else _timestamp(execution_started_at, field="execution_started_at")
    )
    if start < search_completed:
        _fail("execution_before_acquisition", "production starts before acquisition completed")
    if start >= search_completed + timedelta(seconds=FRESHNESS_MAX_AGE_SECONDS):
        _fail("stale_literature", "production starts outside the sealed freshness window")
    start_text = _iso(start)

    implementations = {
        stage_id: _implementation(stage_id, code_root)
        for stage_id in ORDERED_STAGE_IDS
    }
    schema_identity = _code_file_identity(
        code_root, SCHEMA_RELATIVE_PATH, role="manifest_schema"
    )
    catalog = _theory_catalog(snapshot)
    algorithm_contracts = _algorithm_contracts(implementations, catalog)

    stages: list[dict[str, Any]] = []
    acquisition_stage = _stage_record(
        stage_index=0,
        stage_id="acquisition_reopen",
        identity=identity,
        implementation=implementations["acquisition_reopen"],
        input_bindings=[
            _binding(
                "exact_source_bundle",
                source_bundle["bundle_digest"],
                source_artifact_path=CAPTURE_NAME,
            )
        ],
        output_role="validated_acquisition_authority",
        output_payload=acquisition_authority,
        output_schema=None,
        started_at=str(capture["capture_started_at"]),
        completed_at=str(snapshot["search_completed_at"]),
        authority_boundary=(
            "Exact checked-in byte validation and reconstruction only; no live renewal, "
            "provider authentication, source truth, latestness, or exhaustiveness."
        ),
    )
    acquisition_producer_receipt = {
        "receipt_id": acquisition_stage["receipt"]["receipt_id"],
        "status": "succeeded",
        "identity": copy.deepcopy(identity),
        "completed_at": str(snapshot["search_completed_at"]),
    }
    acquisition_stage["receipt"]["native_receipt"] = copy.deepcopy(
        acquisition_producer_receipt
    )
    stages.append(acquisition_stage)

    policy = build_source_routing_pre_map_policy(
        authority=acquisition_authority,
        snapshot=snapshot,
        target_id=TARGET_ID,
        run_id=RUN_ID,
        state_version=STATE_VERSION,
        acquisition_producer_receipt=acquisition_producer_receipt,
        algorithm_contracts=algorithm_contracts,
        sealed_at=start_text,
        freshness_max_age_seconds=FRESHNESS_MAX_AGE_SECONDS,
    )
    validate_source_routing_pre_map_policy(
        policy,
        authority=acquisition_authority,
        snapshot=snapshot,
        acquisition_producer_receipt=acquisition_producer_receipt,
        algorithm_contracts=algorithm_contracts,
    )
    policy_stage = _stage_record(
        stage_index=1,
        stage_id="source_pre_map_policy",
        identity=identity,
        implementation=implementations["source_pre_map_policy"],
        input_bindings=[
            _binding(
                "validated_acquisition_authority",
                acquisition_stage["output"]["content_digest"],
                source_stage_id="acquisition_reopen",
            ),
            _binding("literature_snapshot", snapshot["content_digest"], source_artifact_path=ACQUISITION_NAME),
            _binding("algorithm_contracts", canonical_digest(algorithm_contracts)),
        ],
        output_role="source_routing_pre_map_policy",
        output_payload=policy,
        output_schema="agentic/spec/source_routing_pre_map_policy.schema.json",
        started_at=start_text,
        completed_at=start_text,
        authority_boundary=(
            "Local unregistered pre-map policy execution only; no source truth, "
            "positive support, novelty, conceptual merit, or investment authority."
        ),
    )
    stages.append(policy_stage)

    warrant_packet = build_source_routing_warrant_validation_packet(
        policy=policy,
        snapshot=snapshot,
    )
    validate_source_routing_warrant_validation_packet(
        warrant_packet,
        policy=policy,
        snapshot=snapshot,
    )
    mapping_derivation = derive_claim_mappings(snapshot, theory_catalog=catalog)
    validate_claim_mapping_derivation(
        mapping_derivation,
        snapshot=snapshot,
        theory_catalog=catalog,
    )
    assimilation_completed_at = _iso(start + timedelta(seconds=6))
    assimilation = assimilate_derived_literature(
        snapshot,
        theory_catalog=catalog,
        mapping_derivation=mapping_derivation,
        freshness_max_age_seconds=FRESHNESS_MAX_AGE_SECONDS,
        freshness_evaluated_at=assimilation_completed_at,
    )
    validate_assimilation(assimilation, snapshot=snapshot)
    requirements = source_routing_realization_requirements(
        policy=policy,
        snapshot=snapshot,
        validated_warrants=warrant_packet["validated_warrants"],
        claim_mappings=mapping_derivation["theory_mappings"],
        assimilation=assimilation,
    )
    native_receipts = _native_source_receipts(
        policy=policy,
        requirements=requirements,
        identity=identity,
        start=start,
    )
    native_by_stage = {row["stage"]: row for row in native_receipts}

    warrant_stage = _stage_record(
        stage_index=2,
        stage_id="warrant_validation",
        identity=identity,
        implementation=implementations["warrant_validation"],
        input_bindings=[
            _binding("pre_map_policy", policy["policy_digest"], source_stage_id="source_pre_map_policy"),
            _binding("literature_snapshot", snapshot["content_digest"], source_artifact_path=ACQUISITION_NAME),
        ],
        output_role="source_routing_warrant_validation_packet",
        output_payload=warrant_packet,
        output_schema="agentic/spec/source_routing_warrant_validation_packet.schema.json",
        started_at=native_by_stage["warrant_validation"]["started_at"],
        completed_at=native_by_stage["warrant_validation"]["completed_at"],
        authority_boundary=(
            "Deterministic policy-bound warrant projection only; empty explicit "
            "warrants remain an explicit null and no semantic entailment is inferred."
        ),
        native_receipt=native_by_stage["warrant_validation"],
    )
    stages.append(warrant_stage)

    mapping_output = {
        "theory_object_catalog": catalog,
        "mapping_derivation": mapping_derivation,
    }
    mapping_stage = _stage_record(
        stage_index=3,
        stage_id="claim_mapping",
        identity=identity,
        implementation=implementations["claim_mapping"],
        input_bindings=[
            _binding("pre_map_policy", policy["policy_digest"], source_stage_id="source_pre_map_policy"),
            _binding("warrant_validation", warrant_packet["packet_digest"], source_stage_id="warrant_validation"),
            _binding("theory_object_catalog", catalog["content_digest"]),
            _binding("literature_snapshot", snapshot["content_digest"], source_artifact_path=ACQUISITION_NAME),
        ],
        output_role="literature_claim_mapping_derivation",
        output_payload=mapping_output,
        output_schema="agentic/spec/literature_claim_mapping_stage_output.schema.json",
        started_at=native_by_stage["claim_mapping"]["started_at"],
        completed_at=native_by_stage["claim_mapping"]["completed_at"],
        authority_boundary=(
            "Deterministic internal unresolved/correction routing only; no source "
            "truth, semantic entailment, novelty, exhaustive coverage, or merit."
        ),
        native_receipt=native_by_stage["claim_mapping"],
    )
    stages.append(mapping_stage)

    assimilation_stage = _stage_record(
        stage_index=4,
        stage_id="assimilation",
        identity=identity,
        implementation=implementations["assimilation"],
        input_bindings=[
            _binding("pre_map_policy", policy["policy_digest"], source_stage_id="source_pre_map_policy"),
            _binding("warrant_validation", warrant_packet["packet_digest"], source_stage_id="warrant_validation"),
            _binding("claim_mapping_derivation", mapping_derivation["content_digest"], source_stage_id="claim_mapping"),
            _binding("literature_snapshot", snapshot["content_digest"], source_artifact_path=ACQUISITION_NAME),
        ],
        output_role="literature_assimilation_packet",
        output_payload=assimilation,
        output_schema="agentic/spec/literature_assimilation_packet.schema.json",
        started_at=native_by_stage["assimilation"]["started_at"],
        completed_at=native_by_stage["assimilation"]["completed_at"],
        authority_boundary=(
            "Local theory-routing effects and explicit nulls only; no claim that the "
            "sources are correct or that literature improved conceptual discovery."
        ),
        native_receipt=native_by_stage["assimilation"],
    )
    stages.append(assimilation_stage)

    realization_completed_at = _iso(start + timedelta(seconds=8))
    realization = build_source_routing_realization(
        policy=policy,
        authority=acquisition_authority,
        snapshot=snapshot,
        acquisition_producer_receipt=acquisition_producer_receipt,
        algorithm_contracts=algorithm_contracts,
        validated_warrants=warrant_packet["validated_warrants"],
        claim_mappings=mapping_derivation["theory_mappings"],
        assimilation=assimilation,
        stage_receipts=native_receipts,
        completed_at=realization_completed_at,
    )
    validate_source_routing_realization(
        realization,
        policy=policy,
        authority=acquisition_authority,
        snapshot=snapshot,
        acquisition_producer_receipt=acquisition_producer_receipt,
        algorithm_contracts=algorithm_contracts,
        validated_warrants=warrant_packet["validated_warrants"],
        claim_mappings=mapping_derivation["theory_mappings"],
        assimilation=assimilation,
        stage_receipts=native_receipts,
    )
    realization_stage = _stage_record(
        stage_index=5,
        stage_id="source_routing_realization",
        identity=identity,
        implementation=implementations["source_routing_realization"],
        input_bindings=[
            _binding("pre_map_policy", policy["policy_digest"], source_stage_id="source_pre_map_policy"),
            _binding("warrant_validation", warrant_packet["packet_digest"], source_stage_id="warrant_validation"),
            _binding("claim_mapping_derivation", mapping_derivation["content_digest"], source_stage_id="claim_mapping"),
            _binding("assimilation", assimilation["content_digest"], source_stage_id="assimilation"),
            _binding("ordered_native_stage_receipts", canonical_digest(native_receipts)),
        ],
        output_role="source_routing_realization",
        output_payload=realization,
        output_schema="agentic/spec/source_routing_realization.schema.json",
        started_at=_iso(start + timedelta(seconds=7)),
        completed_at=realization_completed_at,
        authority_boundary=(
            "Two-phase local routing realization only; this source authority does "
            "not create conceptual preference or world-commissioning authority."
        ),
    )
    stages.append(realization_stage)

    portfolio = forge_high_risk_portfolio(
        _high_risk_charter(snapshot),
        snapshot,
        requested_count=10,
        relevance_floor=0.70,
    )
    high_risk_stage = _stage_record(
        stage_index=6,
        stage_id="high_risk_input",
        identity=identity,
        implementation=implementations["high_risk_input"],
        input_bindings=[
            _binding("source_routing_realization", realization["realization_digest"], source_stage_id="source_routing_realization"),
            _binding("assimilation", assimilation["content_digest"], source_stage_id="assimilation"),
            _binding("literature_snapshot", snapshot["content_digest"], source_artifact_path=ACQUISITION_NAME),
        ],
        output_role="high_risk_hypothesis_portfolio",
        output_payload=portfolio,
        output_schema="agentic/spec/high_risk_hypothesis_portfolio.schema.json",
        started_at=_iso(start + timedelta(seconds=9)),
        completed_at=_iso(start + timedelta(seconds=10)),
        producer_authority="local_registered_operator_execution",
        reason_codes=["authored_fallback_not_proposal_field_free"],
        authority_boundary=(
            "The existing authored fallback was executed and literature-rebased; it "
            "does not establish proposal-field-free creativity, novelty, depth, or merit."
        ),
    )
    stages.append(high_risk_stage)

    reflection_input = _reflection_request(
        snapshot=snapshot,
        assimilation=assimilation,
        portfolio=portfolio,
        operator_receipt_ids=[
            acquisition_stage["receipt"]["receipt_id"],
            realization_stage["receipt"]["receipt_id"],
            high_risk_stage["receipt"]["receipt_id"],
        ],
    )
    parent_completed_at = _iso(start + timedelta(seconds=12))
    parent_packet = _execute_reflective_operator(
        operator_id="reflective-conceptual-discovery",
        stage="full",
        envelope=reflection_input,
        created_at=parent_completed_at,
        code_root=code_root,
    )
    parent_stage = _stage_record(
        stage_index=7,
        stage_id="parent_reflection",
        identity=identity,
        implementation=implementations["parent_reflection"],
        input_bindings=[
            _binding("source_routing_realization", realization["realization_digest"], source_stage_id="source_routing_realization"),
            _binding("high_risk_portfolio", portfolio["content_digest"], source_stage_id="high_risk_input"),
            _binding("assimilation", assimilation["content_digest"], source_stage_id="assimilation"),
        ],
        output_role="parent_reflective_conceptual_discovery_packet",
        output_payload=parent_packet,
        output_schema="agentic/spec/reflective_conceptual_discovery_packet.schema.json",
        started_at=_iso(start + timedelta(seconds=11)),
        completed_at=parent_completed_at,
        producer_authority="local_registered_operator_execution",
        reason_codes=["local_structural_fallback"],
        authority_boundary=(
            "Diagnostic local reflection only; no sealed conceptual preference, external "
            "creativity, understanding gain, physics value, proof, or experiment authority."
        ),
    )
    stages.append(parent_stage)

    parent_adjudication_completed_at = _iso(start + timedelta(seconds=14))
    parent_evidence, typed_parent_systems = _execute_conceptual_adjudication(
        stage_id="parent-conceptual-adjudication",
        proposal_packet=parent_packet,
        proposal_receipt_ids=[parent_stage["receipt"]["receipt_id"]],
        snapshot=snapshot,
        portfolio=portfolio,
        proposer_identity="reflective-conceptual-discovery",
        previous_evidence=None,
        created_at=parent_adjudication_completed_at,
        code_root=code_root,
    )
    parent_adjudication_stage = _stage_record(
        stage_index=8,
        stage_id="parent_conceptual_adjudication",
        identity=identity,
        implementation=implementations["parent_conceptual_adjudication"],
        input_bindings=[
            _binding("parent_reflection", parent_packet["packet_digest"], source_stage_id="parent_reflection"),
            _binding("high_risk_portfolio", portfolio["content_digest"], source_stage_id="high_risk_input"),
            _binding("literature_snapshot", snapshot["content_digest"], source_artifact_path=ACQUISITION_NAME),
        ],
        derived_intermediates=[
            _derived_intermediate(
                "typed_conceptual_systems",
                typed_parent_systems,
                derived_from_input_roles=["parent_reflection"],
            )
        ],
        output_role="parent_conceptual_adjudication_evidence",
        output_payload=parent_evidence,
        output_schema="agentic/spec/conceptual_adjudication_evidence.schema.json",
        started_at=_iso(start + timedelta(seconds=13)),
        completed_at=parent_adjudication_completed_at,
        producer_authority="local_registered_operator_execution",
        reason_codes=[
            "correlated_internal_critic_panel",
            "external_human_evidence_unavailable",
        ],
        authority_boundary=(
            "Registered blind adjudication with typed graphs and three deep lenses; "
            "the panel is internally correlated and grants no external, independent, "
            "truth, proof, publication, experiment, or physics-value authority."
        ),
    )
    stages.append(parent_adjudication_stage)

    synthesis_envelope = {
        **copy.deepcopy(reflection_input),
        "prior_reflective_packet": copy.deepcopy(parent_packet),
        "conceptual_systems": copy.deepcopy(typed_parent_systems),
        "reflection_rounds": copy.deepcopy(parent_packet["reflection_rounds"]),
        "generation_mode": "operator_generated",
        "previous_evidence": copy.deepcopy(parent_evidence),
        "request_theory_support_probe": False,
    }
    synthesis_completed_at = _iso(start + timedelta(seconds=16))
    synthesis_packet = _execute_reflective_operator(
        operator_id="reflective-theory-synthesizer",
        stage="reflect",
        envelope=synthesis_envelope,
        created_at=synthesis_completed_at,
        code_root=code_root,
    )
    synthesis_stage = _stage_record(
        stage_index=9,
        stage_id="theory_only_synthesis",
        identity=identity,
        implementation=implementations["theory_only_synthesis"],
        input_bindings=[
            _binding("parent_reflection", parent_packet["packet_digest"], source_stage_id="parent_reflection"),
            _binding("parent_adjudication_evidence", parent_evidence["evidence_digest"], source_stage_id="parent_conceptual_adjudication"),
            _binding("source_routing_realization", realization["realization_digest"], source_stage_id="source_routing_realization"),
        ],
        output_role="parent-evidence-bound_theory_only_synthesis_packet",
        output_payload=synthesis_packet,
        output_schema="agentic/spec/reflective_conceptual_discovery_packet.schema.json",
        started_at=_iso(start + timedelta(seconds=15)),
        completed_at=synthesis_completed_at,
        producer_authority="local_registered_operator_execution",
        reason_codes=[
            "exact_parent_adjudication_consumed",
            "theory_only_no_experiment_input",
        ],
        authority_boundary=(
            "Theory-only synthesis consumed the exact internally correlated parent "
            "evidence without experiment input; it may organize local theory only and "
            "cannot authorize external merit, proof, publication, or world commissioning."
        ),
    )
    stages.append(synthesis_stage)

    synthesis_adjudication_completed_at = _iso(start + timedelta(seconds=18))
    synthesis_evidence, typed_synthesis_systems = _execute_conceptual_adjudication(
        stage_id="synthesis-conceptual-adjudication",
        proposal_packet=synthesis_packet,
        proposal_receipt_ids=[synthesis_stage["receipt"]["receipt_id"]],
        snapshot=snapshot,
        portfolio=portfolio,
        proposer_identity="reflective-theory-synthesizer",
        previous_evidence=parent_evidence,
        created_at=synthesis_adjudication_completed_at,
        code_root=code_root,
    )
    synthesis_adjudication_stage = _stage_record(
        stage_index=10,
        stage_id="synthesis_conceptual_adjudication",
        identity=identity,
        implementation=implementations["synthesis_conceptual_adjudication"],
        input_bindings=[
            _binding("theory_only_synthesis", synthesis_packet["packet_digest"], source_stage_id="theory_only_synthesis"),
            _binding("parent_adjudication_evidence", parent_evidence["evidence_digest"], source_stage_id="parent_conceptual_adjudication"),
            _binding("literature_snapshot", snapshot["content_digest"], source_artifact_path=ACQUISITION_NAME),
        ],
        derived_intermediates=[
            _derived_intermediate(
                "typed_conceptual_systems",
                typed_synthesis_systems,
                derived_from_input_roles=["theory_only_synthesis"],
            )
        ],
        output_role="synthesis_conceptual_adjudication_evidence",
        output_payload=synthesis_evidence,
        output_schema="agentic/spec/conceptual_adjudication_evidence.schema.json",
        started_at=_iso(start + timedelta(seconds=17)),
        completed_at=synthesis_adjudication_completed_at,
        producer_authority="local_registered_operator_execution",
        reason_codes=[
            "correlated_internal_critic_panel",
            "external_human_evidence_unavailable",
            "exact_parent_evidence_bound_for_stage_comparison",
        ],
        authority_boundary=(
            "Registered synthesis adjudication exactly binds the complete parent "
            "evidence, typed graphs, and correlated deep-lens reports; it grants no "
            "external, independent, truth, proof, or world-commissioning authority."
        ),
    )
    stages.append(synthesis_adjudication_stage)

    stage_order_material = [
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
    manifest = {
        "schema_version": "1.0.0",
        "manifest_id": stable_identifier(
            "literature-production-chain",
            source_bundle["bundle_digest"],
            start_text,
            stage_order_material,
        ),
        "chain_kind": "publication_disabled_exact_literature_to_theory",
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "state_version": STATE_VERSION,
        "execution_started_at": start_text,
        "publication_enabled": False,
        "world_commissioning_authorized": False,
        "chain_status": "completed_before_world_commissioning",
        "source_bundle": source_bundle,
        "schema_identity": schema_identity,
        "ordered_stage_ids": list(ORDERED_STAGE_IDS),
        "stages": stages,
        "chain_order_digest": canonical_digest(stage_order_material),
        "claim_boundaries": {
            "bounded_local_production_causality": True,
            "source_truth_authorized": False,
            "global_latestness_authorized": False,
            "exhaustive_coverage_authorized": False,
            "literature_benefit_authorized": False,
            "internal_correlated_conceptual_adjudication_executed": True,
            "external_or_independent_conceptual_preference_authorized": False,
            "internal_deep_lens_adjudication_executed": True,
            "creativity_or_depth_authorized": False,
            "physics_value_authorized": False,
            "theorem_or_yang_mills_result_authorized": False,
            "independent_producer_or_evaluator_authorized": False,
            "experiments_executed": False,
        },
    }
    manifest["manifest_digest"] = canonical_digest(manifest)
    return manifest


def _validate_manifest_structure(manifest: Mapping[str, Any]) -> None:
    """Check cross-field invariants that JSON Schema cannot express compactly."""

    if manifest.get("manifest_digest") != canonical_digest(
        _manifest_without_digest(manifest)
    ):
        _fail("manifest_digest_mismatch", "manifest top-level digest mismatch")
    stages = list(manifest["stages"])
    observed_ids = [row["stage_id"] for row in stages]
    if observed_ids != list(ORDERED_STAGE_IDS):
        _fail("stage_order_invalid", "stages were omitted, duplicated, or reordered")
    if list(manifest["ordered_stage_ids"]) != observed_ids:
        _fail("stage_index_mismatch", "ordered stage index differs from stage records")
    if [row["stage_index"] for row in stages] != list(range(len(ORDERED_STAGE_IDS))):
        _fail("stage_index_invalid", "stage indices are not contiguous and exact")
    for row in stages:
        if row["request"]["stage_id"] != row["stage_id"]:
            _fail("stage_request_substitution", "stage request names another stage")
        if row["receipt"]["request_id"] != row["request"]["request_id"]:
            _fail("stage_receipt_substitution", "stage receipt names another request")
        if row["status"] != row["receipt"]["status"]:
            _fail("stage_status_mismatch", "stage and receipt statuses differ")
        if row["output"]["content_digest"] != canonical_digest(
            row["output"]["payload"]
        ):
            _fail("stage_output_digest_mismatch", f"stage {row['stage_id']} output drifted")
    if any(row["status"] != "succeeded" for row in stages):
        _fail("stage_status_set_invalid", "all eleven production stages must succeed")
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
        _fail("chain_order_digest_mismatch", "ordered causal chain digest mismatch")


def build_publication_disabled_literature_production_chain(
    authority_root: Path = DEFAULT_AUTHORITY_ROOT,
    *,
    code_root: Path = CODE_ROOT,
    execution_started_at: str | None = None,
) -> dict[str, Any]:
    """Execute the bounded local chain and return its strict manifest.

    ``authority_root`` must contain the exact capture, acquisition, and six raw
    response files.  ``execution_started_at`` is an injected clock used only to
    prove ordering and bounded use; it cannot renew the acquisition.  The
    returned object is validated and complete, but commissioning remains forbidden.
    """

    manifest = _build_manifest(
        authority_root=authority_root,
        code_root=code_root.resolve(strict=True),
        execution_started_at=execution_started_at,
    )
    validate_payload(manifest, SCHEMA_NAME)
    _validate_manifest_structure(manifest)
    return manifest


def validate_literature_production_chain_manifest(
    manifest: Mapping[str, Any],
    *,
    authority_root: Path = DEFAULT_AUTHORITY_ROOT,
    code_root: Path = CODE_ROOT,
) -> dict[str, Any]:
    """Reexecute every available stage and reject any manifest substitution."""

    observed = copy.deepcopy(dict(manifest))
    validate_payload(observed, SCHEMA_NAME)
    _validate_manifest_structure(observed)
    if (
        observed.get("target_id") != TARGET_ID
        or observed.get("run_id") != RUN_ID
        or observed.get("state_version") != STATE_VERSION
    ):
        _fail("chain_identity_mismatch", "manifest crossed the fixed target/run/state")
    expected = _build_manifest(
        authority_root=authority_root,
        code_root=code_root.resolve(strict=True),
        execution_started_at=str(observed["execution_started_at"]),
    )
    validate_payload(expected, SCHEMA_NAME)
    _validate_manifest_structure(expected)
    if observed != expected:
        _fail(
            "manifest_replay_mismatch",
            "manifest differs from exact source, code, dependency, and stage replay",
        )
    return observed


__all__ = [
    "ACQUISITION_NAME",
    "CAPTURE_NAME",
    "CODE_ROOT",
    "DEFAULT_AUTHORITY_ROOT",
    "LiteratureProductionChainError",
    "ORDERED_STAGE_IDS",
    "RUN_ID",
    "STATE_VERSION",
    "TARGET_ID",
    "build_publication_disabled_literature_production_chain",
    "validate_literature_production_chain_manifest",
]
