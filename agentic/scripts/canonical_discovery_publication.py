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
"""Canonical DWF profile for the reusable content-addressed publisher.

The public functions retain the original DWF call surface.  Storage, locking,
separate core/evidence identity, immutable index snapshots, history, and legacy
retention are provided by :mod:`canonical_publication_engine`.  This module is
only the trusted DWF validation/evidence profile; target-specific profiles can
reuse the same engine without being imported from untrusted index data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from agentic_common import ROOT

from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.dependency_authority import build_dependency_authority
from canonical_publication_engine import (
    PublicationProfile,
    PublicationSource,
    plan_profile_publication,
    publish_profile_current,
    resolve_profile_current,
    validate_profile_current,
)
from discovery_operator_registry import REGISTRY_PATH
from generate_canonical_discovery_release import build_release
from run_skill_reachability_audit import build_reachability_report, render_markdown
from validate_canonical_discovery_acceptance import validate_canonical_acceptance
from validate_target_navigation_release import validate_release_receipt


DEFAULT_PUBLICATION_ROOT = ROOT / "agentic/reports/canonical_discovery_cycle/acceptance"
DWF_PROFILE_ID = "canonical-dwf"
DWF_PROFILE_VERSION = "2.0.0"
DWF_AUTHORITY_BOUNDARY = (
    "Exact DWF core/evidence replay and current local implementation authority only; "
    "no source truth, theorem, independent philosophical depth, understanding, or "
    "discovery-efficacy authority."
)

_DWF_ENTRY_PATHS: dict[str, tuple[str, ...]] = {
    "agentic/scripts/canonical_publication_engine.py": ("publication_engine",),
    "agentic/scripts/canonical_discovery_publication.py": ("dwf_profile",),
    "agentic/scripts/validate_canonical_discovery_publication.py": (
        "publication_validation_cli",
    ),
    "agentic/scripts/publish_canonical_discovery_acceptance.py": (
        "publication_write_cli",
    ),
    "agentic/scripts/validate_canonical_discovery_acceptance.py": (
        "core_acceptance_validator",
    ),
    "agentic/scripts/generate_canonical_discovery_release.py": (
        "release_evidence_builder",
    ),
    "agentic/scripts/run_skill_reachability_audit.py": (
        "reachability_evidence_builder",
    ),
}

_DWF_SEMANTIC_PATHS: dict[str, tuple[str, ...]] = {
    "agentic/registries/discovery_operator_registry.yaml": ("operator_registry",),
    "agentic/spec/canonical_discovery_publication_index.schema.json": (
        "publication_index_schema",
    ),
    "agentic/spec/canonical_discovery_content_manifest.schema.json": (
        "content_manifest_schema",
    ),
    "agentic/spec/canonical_publication_profile_authority.schema.json": (
        "profile_authority_schema",
    ),
    "pyproject.toml": ("locked_project_configuration",),
    "uv.lock": ("locked_runtime_resolution",),
}


def _registry_relative(registry_path: Path) -> str:
    resolved = registry_path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ContractError("DWF publication registry must be repository-local") from exc


def _registry_at(authority_root: Path, relative: str) -> Path:
    path = authority_root / relative
    if path.is_symlink() or not path.is_file():
        raise ContractError(f"DWF publication registry is absent or linked: {relative}")
    return path


def build_dwf_profile(registry_path: Path = REGISTRY_PATH) -> PublicationProfile:
    """Build the one trusted DWF profile; never resolve a profile from index bytes."""

    registry_relative = _registry_relative(registry_path)
    semantic_paths = dict(_DWF_SEMANTIC_PATHS)
    semantic_paths[registry_relative] = ("selected_operator_registry",)

    def authority_builder(authority_root: Path) -> Mapping[str, Any]:
        return build_dependency_authority(
            scope="canonical_dwf_publication_profile_v2",
            entry_python_paths=_DWF_ENTRY_PATHS,
            semantic_paths=semantic_paths,
            authority_boundary=DWF_AUTHORITY_BOUNDARY,
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
        return validate_canonical_acceptance(
            cycle_path=Path(locators["cycle_path"]),
            cycle_request_path=Path(locators["cycle_request_path"]),
            state_root=Path(locators["state_root"]),
            workspace=Path(locators["workspace"]),
            receipt_root=Path(locators["receipt_root"]),
            target_id=str(locators["target_id"]),
            run_id=str(locators["run_id"]),
            registry_path=_registry_at(authority_root, registry_relative),
            authority_repository_root=authority_root,
        )

    def evidence_payloads(
        locators: Mapping[str, Any], authority_root: Path
    ) -> Mapping[str, bytes]:
        kwargs = {
            "cycle_path": Path(locators["cycle_path"]),
            "cycle_request_path": Path(locators["cycle_request_path"]),
            "state_root": Path(locators["state_root"]),
            "workspace": Path(locators["workspace"]),
            "receipt_root": Path(locators["receipt_root"]),
            "target_id": str(locators["target_id"]),
            "run_id": str(locators["run_id"]),
        }
        bundle_root = Path(locators["cycle_path"]).parent.resolve()

        def logicalize(value: Any) -> Any:
            """Project physical staging paths into bundle-relative locators."""

            if isinstance(value, Mapping):
                return {key: logicalize(child) for key, child in value.items()}
            if isinstance(value, list):
                return [logicalize(child) for child in value]
            if isinstance(value, str):
                candidate = Path(value)
                if candidate.is_absolute():
                    try:
                        return candidate.resolve().relative_to(bundle_root).as_posix()
                    except ValueError:
                        pass
            return value

        acceptance = logicalize(core_validator(locators, authority_root))
        reachability = logicalize(build_reachability_report(
            receipt_root=kwargs["receipt_root"],
            artifact_root=kwargs["workspace"],
            canonical_cycle_path=kwargs["cycle_path"],
            canonical_state_root=kwargs["state_root"],
            target_id=kwargs["target_id"],
            run_id=kwargs["run_id"],
        ))
        authorization = reachability.get("canonical_authorization")
        if isinstance(authorization, dict):
            authorization["portable_projection_digest"] = canonical_digest(
                authorization, exclude_keys=("portable_projection_digest",)
            )
        release = logicalize(build_release(**kwargs))
        for validator in release["validator_receipts"]:
            receipt_id = str(validator["receipt_id"])
            if ".canonical-acceptance." in receipt_id:
                validator["output_digest"] = canonical_digest(acceptance)
            elif ".operator-feedback." in receipt_id:
                validator["output_digest"] = canonical_digest(reachability)
        release["receipt_digest"] = canonical_digest(
            release, exclude_keys=("receipt_digest",)
        )
        validate_release_receipt(release)
        from canonical_publication_engine import _json_bytes  # trusted local helper

        return {
            "acceptance-summary.json": _json_bytes(acceptance),
            "navigation-release.json": _json_bytes(release),
            "reachability-report.json": _json_bytes(reachability),
            "reachability-report.md": render_markdown(reachability).encode("utf-8"),
        }

    def evidence_validator(
        locators: Mapping[str, Any], evidence_root: Path, authority_root: Path
    ) -> Mapping[str, Any]:
        expected = evidence_payloads(locators, authority_root)
        for relative, encoded in expected.items():
            path = evidence_root / relative
            if path.is_symlink() or not path.is_file() or path.read_bytes() != encoded:
                raise ContractError(
                    f"published DWF evidence differs from exact replay: {relative}"
                )
        acceptance = json.loads(expected["acceptance-summary.json"])
        reachability = json.loads(expected["reachability-report.json"])
        return {
            "status": "validated",
            "acceptance": acceptance,
            "all_operators_feedback_effective": reachability[
                "all_operators_feedback_effective"
            ],
        }

    return PublicationProfile(
        profile_id=DWF_PROFILE_ID,
        profile_version=DWF_PROFILE_VERSION,
        bundle_prefix="dwf",
        authority_boundary=DWF_AUTHORITY_BOUNDARY,
        build_authority=authority_builder,
        validate_core=core_validator,
        build_evidence=evidence_payloads,
        validate_evidence=evidence_validator,
        semantic_contract={
            "profile_kind": "canonical_dwf_v2",
            "registry_path": registry_relative,
            "evidence_locator_mode": "logical_bundle_relative",
            "current_validator_policy": "exact_repository_authority",
        },
    )


def _source(
    *,
    cycle_path: Path,
    cycle_request_path: Path,
    state_root: Path,
    workspace: Path,
    receipt_root: Path,
    target_id: str,
    run_id: str,
) -> PublicationSource:
    return PublicationSource(
        cycle_path=cycle_path,
        state_root=state_root,
        workspace=workspace,
        target_id=target_id,
        run_id=run_id,
        workspace_locators={
            "cycle_request_path": cycle_request_path,
            "receipt_root": receipt_root,
        },
    )


def plan_publication(
    *,
    cycle_path: Path,
    cycle_request_path: Path,
    state_root: Path,
    workspace: Path,
    receipt_root: Path,
    target_id: str,
    run_id: str,
    publication_root: Path = DEFAULT_PUBLICATION_ROOT,
    legacy_bundle: Path | None = None,
    registry_path: Path = REGISTRY_PATH,
    authority_repository_root: Path = ROOT,
) -> dict[str, Any]:
    result = plan_profile_publication(
        source=_source(
            cycle_path=cycle_path,
            cycle_request_path=cycle_request_path,
            state_root=state_root,
            workspace=workspace,
            receipt_root=receipt_root,
            target_id=target_id,
            run_id=run_id,
        ),
        profile=build_dwf_profile(registry_path),
        publication_root=publication_root,
        legacy_bundle=legacy_bundle,
        legacy_label="active-current-registry",
        authority_repository_root=authority_repository_root,
    )
    result["acceptance_status"] = result["core_validation_status"]
    return result


def publish_current(
    *,
    cycle_path: Path,
    cycle_request_path: Path,
    state_root: Path,
    workspace: Path,
    receipt_root: Path,
    target_id: str,
    run_id: str,
    publication_root: Path = DEFAULT_PUBLICATION_ROOT,
    legacy_bundle: Path | None = None,
    registry_path: Path = REGISTRY_PATH,
    authority_repository_root: Path = ROOT,
) -> dict[str, Any]:
    return publish_profile_current(
        source=_source(
            cycle_path=cycle_path,
            cycle_request_path=cycle_request_path,
            state_root=state_root,
            workspace=workspace,
            receipt_root=receipt_root,
            target_id=target_id,
            run_id=run_id,
        ),
        profile=build_dwf_profile(registry_path),
        publication_root=publication_root,
        legacy_bundle=legacy_bundle,
        legacy_label="active-current-registry",
        authority_repository_root=authority_repository_root,
    )


def resolve_current_publication(
    publication_root: Path = DEFAULT_PUBLICATION_ROOT,
    *,
    registry_path: Path = REGISTRY_PATH,
) -> dict[str, Any]:
    return resolve_profile_current(
        publication_root=publication_root,
        profile=build_dwf_profile(registry_path),
    )


def validate_current_publication(
    *,
    publication_root: Path = DEFAULT_PUBLICATION_ROOT,
    registry_path: Path = REGISTRY_PATH,
    authority_repository_root: Path = ROOT,
) -> dict[str, Any]:
    result = validate_profile_current(
        publication_root=publication_root,
        profile=build_dwf_profile(registry_path),
        authority_repository_root=authority_repository_root,
    )
    evidence = result["evidence_validation"]
    return {
        **result,
        "acceptance": evidence["acceptance"],
        "all_operators_feedback_effective": evidence[
            "all_operators_feedback_effective"
        ],
    }


__all__ = [
    "DEFAULT_PUBLICATION_ROOT",
    "DWF_PROFILE_ID",
    "DWF_PROFILE_VERSION",
    "build_dwf_profile",
    "plan_publication",
    "publish_current",
    "resolve_current_publication",
    "validate_current_publication",
]
