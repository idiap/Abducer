#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Target-specific YM profile for the reusable canonical publisher.

The profile derives its request projection and every report from committed
operator evidence.  Publication replay proves that the literature was current
when the cycle committed, while present-day investment eligibility is computed
separately.  The registered binding selects an immutable index snapshot and is
written only after the complete publication validates.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Mapping

from agentic_common import ROOT

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
    file_digest,
    fsync_directory,
    load_json,
    safe_relative_path,
    stable_identifier,
    validate_instance,
)
from agentic.discovery.dependency_authority import build_dependency_authority
from canonical_publication_engine import (
    BUNDLE_MANIFEST,
    EVIDENCE_MANIFEST,
    INDEX_DIRECTORY,
    PROFILE_AUTHORITY_NAME,
    PublicationProfile,
    PublicationSource,
    _json_bytes,
    _object,
    _resolved_manifest_locators,
    _validate_archives,
    _validate_authority_shape,
    _validate_legacy_publication,
    _validate_row,
    plan_profile_publication,
    publication_lock,
    publish_profile_current,
    resolve_profile_current,
    validate_profile_current,
)
from integrate_ym_representational_dynamics_20260721 import (
    BROAD_FRONTIER_CAPTURE,
    IMPORT_ROOT,
    REGISTERED_RUNTIME_BINDING,
    REPORT_ROOT,
    TARGET_ID,
)
from run_ym_canonical_parent_cycle_20260721 import (
    RUN_ID,
    _build_publication_payloads,
)
from validate_ym_canonical_parent_cycle_20260721 import (
    load_committed_publication_material,
    present_investment_freshness,
)


DEFAULT_YM_PUBLICATION_ROOT = REPORT_ROOT / "canonical_parent_publication"
LEGACY_YM_ROOT = REPORT_ROOT / "canonical_parent_cycle"
SOURCE_MANIFEST = IMPORT_ROOT / "immutable_source_manifest.json"
SOURCE_ARCHIVE = (
    IMPORT_ROOT
    / "source_archives/full ym_representational_dynamics_complete_2026-07-21 (1).zip"
)
YM_PROFILE_ID = "ym-representational-dynamics-20260721"
YM_PROFILE_VERSION = "1.0.0"
YM_AUTHORITY_BOUNDARY = (
    "Exact committed YM conceptual-cycle replay, frozen-source provenance, and internal "
    "structural validation only; no source truth, external efficacy, independent depth, "
    "continuum construction, theorem, or mass-gap authority."
)

_YM_ENTRY_PATHS: dict[str, tuple[str, ...]] = {
    "agentic/scripts/canonical_publication_engine.py": ("publication_engine",),
    "agentic/scripts/ym_canonical_publication_20260721.py": ("ym_profile",),
    "agentic/scripts/publish_ym_canonical_publication_20260721.py": (
        "ym_publication_cli",
    ),
    "agentic/scripts/validate_ym_canonical_publication_20260721.py": (
        "ym_validation_cli",
    ),
    "agentic/scripts/validate_ym_canonical_parent_cycle_20260721.py": (
        "ym_core_validator",
    ),
    "agentic/scripts/run_ym_canonical_parent_cycle_20260721.py": (
        "ym_committed_evidence_builder",
    ),
    "agentic/scripts/evaluate_ym_conceptual_quality_20260721.py": (
        "conceptual_quality_validator",
    ),
}

_YM_SEMANTIC_PATHS: dict[str, tuple[str, ...]] = {
    "agentic/registries/discovery_operator_registry.yaml": ("operator_registry",),
    "agentic/registries/discovery_publication_profiles.yaml": (
        "publication_profile_registry",
    ),
    "agentic/spec/canonical_discovery_publication_index.schema.json": (
        "publication_index_schema",
    ),
    "agentic/spec/canonical_discovery_content_manifest.schema.json": (
        "content_manifest_schema",
    ),
    "agentic/spec/canonical_publication_profile_authority.schema.json": (
        "profile_authority_schema",
    ),
    "agentic/spec/ym_canonical_publication_request.schema.json": (
        "committed_request_projection_schema",
    ),
    "agentic/spec/ym_source_provenance_binding.schema.json": (
        "source_binding_schema",
    ),
    "agentic/spec/ym_registered_publication_binding.schema.json": (
        "registered_binding_schema",
    ),
    "agentic/external/yang_mills_representational_dynamics/2026-07-21/immutable_source_manifest.json": (
        "immutable_source_manifest",
    ),
    "agentic/external/yang_mills_representational_dynamics/2026-07-21/checksum_report.json": (
        "source_checksum_report",
    ),
    "pyproject.toml": ("locked_project_configuration",),
    "uv.lock": ("locked_runtime_resolution",),
}


def _repo_relative(path: Path, label: str) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ContractError(f"{label} must be repository-local") from exc


def _load_object(path: Path, label: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ContractError(f"{label} is absent or linked: {path}")
    value = load_json(path)
    if not isinstance(value, dict):
        raise ContractError(f"{label} must be a JSON object")
    return value


def _material(locators: Mapping[str, Any]) -> dict[str, Any]:
    cycle_path = Path(locators["cycle_path"])
    state_root = Path(locators["state_root"])
    return load_committed_publication_material(
        cycle_path.parent,
        historical_replay=True,
        cycle_path=cycle_path,
        state_root=state_root,
    )


def committed_request_projection(material: Mapping[str, Any]) -> dict[str, Any]:
    result = material["result"]
    core: dict[str, Any] = {
        "schema_version": "1.0.0",
        "request_kind": "ym_committed_operator_projection",
        "target_id": result["target_id"],
        "run_id": result["run_id"],
        "cycle_id": result["cycle_id"],
        "commit_id": result["commit_id"],
        "operator_requests": copy.deepcopy(material["requests"]),
        "operator_receipts": copy.deepcopy(material["receipts"]),
        "artifact_roles": copy.deepcopy(material["artifact_roles"]),
        "derivation": "exactly_reconstructed_from_committed_operator_evidence",
        "authority_boundary": (
            "Portable request projection only; it introduces no uncommitted scientific input."
        ),
    }
    core["content_digest"] = canonical_digest(core)
    validate_instance(core, "ym_canonical_publication_request.schema.json")
    return core


def source_provenance_binding(
    material: Mapping[str, Any], *, authority_root: Path = ROOT
) -> dict[str, Any]:
    manifest_path = authority_root / _repo_relative(SOURCE_MANIFEST, "source manifest")
    archive_path = authority_root / _repo_relative(SOURCE_ARCHIVE, "source archive")
    capture_path = authority_root / _repo_relative(
        BROAD_FRONTIER_CAPTURE, "frontier capture"
    )
    manifest = _load_object(manifest_path, "immutable YM source manifest")
    raw = manifest.get("raw_archive", {})
    if (
        raw.get("repo_path") != _repo_relative(SOURCE_ARCHIVE, "source archive")
        or f"sha256:{raw.get('sha256')}" != file_digest(archive_path)
        or raw.get("size_bytes") != archive_path.stat().st_size
    ):
        raise ContractError("immutable YM source manifest/archive binding drift")
    capture = _load_object(capture_path, "frozen frontier capture")
    freshness = material["core_validation"]
    binding: dict[str, Any] = {
        "schema_version": "1.0.0",
        "target_id": TARGET_ID,
        "source_manifest_path": _repo_relative(SOURCE_MANIFEST, "source manifest"),
        "source_manifest_sha256": file_digest(manifest_path),
        "source_archive_path": _repo_relative(SOURCE_ARCHIVE, "source archive"),
        "source_archive_sha256": file_digest(archive_path),
        "source_archive_size_bytes": archive_path.stat().st_size,
        "frontier_capture_path": _repo_relative(
            BROAD_FRONTIER_CAPTURE, "frontier capture"
        ),
        "frontier_capture_sha256": file_digest(capture_path),
        "frontier_capture_id": capture["capture_id"],
        "coverage_cutoff": capture["coverage_cutoff"],
        "freshness_at_execution": freshness["freshness_at_execution"],
        "search_completed_at": freshness["search_completed_at"],
        "consume_before": freshness["consume_before"],
        "committed_at": freshness["committed_at"],
        "license_status": manifest["license"]["status"],
        "authorship_status": manifest["provenance"]["authorship_status"],
        "authority_boundary": (
            "Binds preserved bytes and the fixed search window only; it does not establish "
            "authorship, license, source truth, exhaustive coverage, or theorem validity."
        ),
    }
    binding["content_digest"] = canonical_digest(binding)
    validate_instance(binding, "ym_source_provenance_binding.schema.json")
    return binding


def build_ym_profile() -> PublicationProfile:
    def authority_builder(authority_root: Path) -> Mapping[str, Any]:
        return build_dependency_authority(
            scope="ym_representational_dynamics_publication_profile_20260721",
            entry_python_paths=_YM_ENTRY_PATHS,
            semantic_paths=_YM_SEMANTIC_PATHS,
            authority_boundary=YM_AUTHORITY_BOUNDARY,
            repository_root=authority_root,
            runtime_distributions={
                "jsonschema": "jsonschema",
                "referencing": "referencing",
                "sympy": "sympy",
            },
        )

    def core_validator(
        locators: Mapping[str, Any], authority_root: Path
    ) -> Mapping[str, Any]:
        material = _material(locators)
        expected_request = committed_request_projection(material)
        request_path = Path(locators["cycle_request_path"])
        request = _load_object(request_path, "portable committed request")
        if request != expected_request:
            raise ContractError(
                "portable YM cycle request differs from committed operator evidence"
            )
        expected_receipt_root = (
            Path(locators["workspace"])
            / "operator-receipts"
            / TARGET_ID
            / RUN_ID
        ).resolve()
        if Path(locators["receipt_root"]).resolve() != expected_receipt_root:
            raise ContractError("portable YM receipt-root locator drift")
        summary = dict(material["core_validation"])
        summary["request_projection_digest"] = request["content_digest"]
        summary["status"] = "validated_core_historical_replay"
        return summary

    def evidence_builder(
        locators: Mapping[str, Any], authority_root: Path
    ) -> Mapping[str, bytes]:
        material = _material(locators)
        request = committed_request_projection(material)
        reports = dict(_build_publication_payloads(material))
        source_binding = source_provenance_binding(
            material, authority_root=authority_root
        )
        validation_summary = dict(material["core_validation"])
        validation_summary.update(
            {
                "status": "validated_historical_publication_source",
                "new_investment_status_semantics": (
                    "computed_at_binding_resolution_from_consume_before; never frozen as active-current"
                ),
                "authority_boundary": YM_AUTHORITY_BOUNDARY,
            }
        )
        reports.update(
            {
                "canonical-cycle-request.json": _json_bytes(request),
                "target-validation-summary.json": _json_bytes(validation_summary),
                "source-provenance-binding.json": _json_bytes(source_binding),
            }
        )
        return reports

    def evidence_validator(
        locators: Mapping[str, Any], evidence_root: Path, authority_root: Path
    ) -> Mapping[str, Any]:
        expected = evidence_builder(locators, authority_root)
        expected_names = set(expected) | {PROFILE_AUTHORITY_NAME, EVIDENCE_MANIFEST}
        actual_names = {
            path.relative_to(evidence_root).as_posix()
            for path in evidence_root.rglob("*")
            if path.is_file()
        }
        if actual_names != expected_names:
            raise ContractError("YM evidence tree has missing or undeclared files")
        for relative, encoded in expected.items():
            path = evidence_root / relative
            if path.is_symlink() or not path.is_file() or path.read_bytes() != encoded:
                raise ContractError(f"YM evidence replay drift: {relative}")
        source_binding = json.loads(expected["source-provenance-binding.json"])
        return {
            "status": "validated",
            "publication_files": len(expected),
            "freshness_at_execution": source_binding["freshness_at_execution"],
            "consume_before": source_binding["consume_before"],
            "source_archive_sha256": source_binding["source_archive_sha256"],
        }

    return PublicationProfile(
        profile_id=YM_PROFILE_ID,
        profile_version=YM_PROFILE_VERSION,
        bundle_prefix="ym",
        authority_boundary=YM_AUTHORITY_BOUNDARY,
        build_authority=authority_builder,
        validate_core=core_validator,
        build_evidence=evidence_builder,
        validate_evidence=evidence_validator,
        semantic_contract={
            "profile_kind": "ym_committed_historical_replay_v1",
            "target_id": TARGET_ID,
            "run_id": RUN_ID,
            "source_manifest_path": _repo_relative(SOURCE_MANIFEST, "source manifest"),
            "source_archive_path": _repo_relative(SOURCE_ARCHIVE, "source archive"),
            "frontier_capture_path": _repo_relative(
                BROAD_FRONTIER_CAPTURE, "frontier capture"
            ),
        },
    )


@contextmanager
def prepared_publication_source(source_root: Path) -> Iterator[PublicationSource]:
    """Copy the workspace and add only a committed-derived request projection."""

    source_root = source_root.resolve()
    cycle_path = source_root / "canonical_cycle_result.json"
    state_root = source_root / "state"
    workspace = source_root / "workspace"
    material = load_committed_publication_material(
        source_root,
        historical_replay=True,
        cycle_path=cycle_path,
        state_root=state_root,
    )
    with tempfile.TemporaryDirectory(prefix="ym-publication-source-") as temporary:
        prepared_workspace = Path(temporary) / "workspace"
        shutil.copytree(workspace, prepared_workspace)
        request_path = prepared_workspace / "canonical-cycle-request.json"
        request_path.write_bytes(
            canonical_json(committed_request_projection(material)) + b"\n"
        )
        receipt_root = (
            prepared_workspace / "operator-receipts" / TARGET_ID / RUN_ID
        )
        if receipt_root.is_symlink() or not receipt_root.is_dir():
            raise ContractError("prepared YM receipt root is absent or linked")
        yield PublicationSource(
            cycle_path=cycle_path,
            state_root=state_root,
            workspace=prepared_workspace,
            target_id=TARGET_ID,
            run_id=RUN_ID,
            workspace_locators={
                "cycle_request_path": request_path,
                "receipt_root": receipt_root,
            },
        )


def plan_ym_publication(
    *,
    source_root: Path,
    publication_root: Path = DEFAULT_YM_PUBLICATION_ROOT,
    legacy_root: Path = LEGACY_YM_ROOT,
    authority_repository_root: Path = ROOT,
) -> dict[str, Any]:
    with prepared_publication_source(source_root) as source:
        return plan_profile_publication(
            source=source,
            profile=build_ym_profile(),
            publication_root=publication_root,
            legacy_bundle=legacy_root,
            legacy_label="ym-canonical-parent-cycle-20260721",
            authority_repository_root=authority_repository_root,
        )


def publish_ym_publication(
    *,
    source_root: Path,
    publication_root: Path = DEFAULT_YM_PUBLICATION_ROOT,
    legacy_root: Path = LEGACY_YM_ROOT,
    authority_repository_root: Path = ROOT,
) -> dict[str, Any]:
    if source_root.resolve() == legacy_root.resolve():
        raise ContractError(
            "the retained legacy YM root cannot also be the fresh publication candidate"
        )
    with prepared_publication_source(source_root) as source:
        return publish_profile_current(
            source=source,
            profile=build_ym_profile(),
            publication_root=publication_root,
            legacy_bundle=legacy_root,
            legacy_label="ym-canonical-parent-cycle-20260721",
            authority_repository_root=authority_repository_root,
        )


def _atomic_binding(path: Path, payload: Mapping[str, Any]) -> None:
    if os.path.lexists(path) and path.is_symlink():
        raise ContractError("registered YM publication binding cannot be a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_json_bytes(payload))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _binding_payload_from_snapshot(
    publication_root: Path, snapshot_path: Path
) -> dict[str, Any]:
    """Rebuild every binding field from one immutable validated snapshot."""

    publication_root = publication_root.resolve(strict=True)
    if publication_root.is_symlink() or not publication_root.is_dir():
        raise ContractError("YM publication root is absent or linked")
    if snapshot_path.is_symlink() or not snapshot_path.is_file():
        raise ContractError("bound YM publication snapshot is absent or linked")
    snapshot_path = snapshot_path.resolve(strict=True)
    try:
        relative_snapshot = snapshot_path.relative_to(publication_root)
    except ValueError as exc:
        raise ContractError("bound YM snapshot escapes its publication root") from exc
    snapshot_sha256 = file_digest(snapshot_path)
    expected_snapshot_path = (
        Path(INDEX_DIRECTORY)
        / f"index-{snapshot_sha256.removeprefix('sha256:')}.json"
    )
    if relative_snapshot != expected_snapshot_path:
        raise ContractError("bound YM snapshot path is not content-addressed")

    profile = build_ym_profile()
    snapshot = _load_object(snapshot_path, "immutable YM publication snapshot")
    validate_instance(snapshot, "canonical_discovery_publication_index.schema.json")
    if snapshot.get("index_kind") != "canonical_discovery_publication_snapshot":
        raise ContractError("bound YM publication index is not an immutable snapshot")
    current = snapshot["current"]
    bundle, evidence, bundle_manifest, _evidence_manifest = _validate_row(
        current, publication_root, profile=profile
    )
    locators = _resolved_manifest_locators(bundle, bundle_manifest["metadata"])
    authority = _validate_authority_shape(profile.build_authority(ROOT))
    if (
        _load_object(evidence / PROFILE_AUTHORITY_NAME, "YM profile authority")
        != authority
        or authority["content_digest"] != current["profile_authority_digest"]
    ):
        raise ContractError("bound YM profile authority drift")
    profile.validate_core(locators, ROOT)
    profile.validate_evidence(locators, evidence, ROOT)

    seen_publications = {(current["bundle_id"], current["evidence_id"])}
    for row in snapshot["history"]:
        identity = (row["bundle_id"], row["evidence_id"])
        if identity in seen_publications:
            raise ContractError("YM snapshot history repeats current or prior evidence")
        seen_publications.add(identity)
        _validate_row(row, publication_root, profile=None)
    for row in snapshot["legacy_publications"]:
        _validate_legacy_publication(row, publication_root)
    _validate_archives(snapshot["legacy_archives"], publication_root)

    source_binding = _load_object(
        evidence / "source-provenance-binding.json",
        "published source binding",
    )
    validate_instance(source_binding, "ym_source_provenance_binding.schema.json")
    unsigned_source = copy.deepcopy(source_binding)
    if unsigned_source.pop("content_digest") != canonical_digest(unsigned_source):
        raise ContractError("published YM source binding digest mismatch")
    payload: dict[str, Any] = {
        "schema_version": "2.0.0",
        "binding_id": stable_identifier(
            "ym-current-publication",
            current["bundle_id"],
            current["evidence_id"],
            snapshot_sha256,
        ),
        "status": "current_publication",
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "cycle_id": current["cycle_id"],
        "commit_id": current["commit_id"],
        "profile_id": profile.profile_id,
        "profile_version": profile.profile_version,
        "profile_authority_digest": current["profile_authority_digest"],
        "publication_root": _repo_relative(publication_root, "publication root"),
        "immutable_index_snapshot_path": _repo_relative(
            snapshot_path, "index snapshot"
        ),
        "immutable_index_snapshot_sha256": snapshot_sha256,
        "bundle_id": current["bundle_id"],
        "bundle_path": _repo_relative(bundle, "bundle"),
        "bundle_manifest_digest": current["bundle_manifest_digest"],
        "evidence_id": current["evidence_id"],
        "evidence_path": _repo_relative(evidence, "evidence"),
        "evidence_manifest_digest": current["evidence_manifest_digest"],
        "locators": {
            name: _repo_relative(Path(locators[name]), name)
            for name in (
                "cycle_path",
                "cycle_request_path",
                "state_root",
                "workspace",
                "receipt_root",
            )
        },
        "legacy_archives": copy.deepcopy(snapshot["legacy_archives"]),
        "source_provenance": source_binding,
        "validation_status": "passed",
        "authority_boundary": (
            "Selects immutable published evidence, not permanently active literature. New theory "
            "investment must recompute freshness and refresh once consume_before has passed. "
            + YM_AUTHORITY_BOUNDARY
        ),
    }
    payload["content_digest"] = canonical_digest(payload)
    validate_instance(payload, "ym_registered_publication_binding.schema.json")
    return payload


def _binding_payload(publication_root: Path) -> dict[str, Any]:
    profile = build_ym_profile()
    validate_profile_current(
        publication_root=publication_root,
        profile=profile,
        authority_repository_root=ROOT,
    )
    resolved = resolve_profile_current(
        publication_root=publication_root, profile=profile
    )
    return _binding_payload_from_snapshot(
        publication_root.resolve(), Path(resolved["snapshot_path"])
    )


def bind_registered_ym_publication(
    publication_root: Path = DEFAULT_YM_PUBLICATION_ROOT,
) -> dict[str, Any]:
    """Validate the selected publication and atomically replace the binding last."""

    with publication_lock(publication_root):
        payload = _binding_payload(publication_root.resolve())
        _atomic_binding(REGISTERED_RUNTIME_BINDING, payload)
    return resolve_registered_ym_publication()


def resolve_registered_ym_publication(
    *, now: dt.datetime | None = None
) -> dict[str, Any]:
    """Validate the bound immutable snapshot, independent of the mutable pointer."""

    binding = _load_object(REGISTERED_RUNTIME_BINDING, "registered YM publication")
    validate_instance(binding, "ym_registered_publication_binding.schema.json")
    unsigned = copy.deepcopy(binding)
    digest = unsigned.pop("content_digest")
    if digest != canonical_digest(unsigned):
        raise ContractError("registered YM publication binding digest mismatch")
    publication_root = safe_relative_path(
        binding["publication_root"], ROOT, forbid_latest=False
    )
    snapshot_path = safe_relative_path(
        binding["immutable_index_snapshot_path"], ROOT, forbid_latest=False
    )
    expected = _binding_payload_from_snapshot(publication_root, snapshot_path)
    if binding != expected:
        raise ContractError(
            "registered YM binding is not the exact immutable-snapshot projection"
        )
    source_binding = expected["source_provenance"]
    resolved = copy.deepcopy(expected)
    resolved["new_investment_status"] = present_investment_freshness(
        source_binding["consume_before"],
        search_completed_at=source_binding["search_completed_at"],
        now=now,
    )
    resolved["binding_authority"] = "immutable_snapshot_current_publication"
    return resolved


__all__ = [
    "DEFAULT_YM_PUBLICATION_ROOT",
    "LEGACY_YM_ROOT",
    "YM_PROFILE_ID",
    "YM_PROFILE_VERSION",
    "bind_registered_ym_publication",
    "build_ym_profile",
    "committed_request_projection",
    "plan_ym_publication",
    "prepared_publication_source",
    "publish_ym_publication",
    "resolve_registered_ym_publication",
    "source_provenance_binding",
]
