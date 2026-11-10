# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Bind finite abstraction evidence to its derived local semantic closure.

The formal forgers, evaluator, validators, and Yang--Mills calibrations import a
substantial shared discovery runtime. A hand-maintained list cannot establish
transitivity, so this profile delegates closure construction to the reusable
repository authority engine. The engine discovers local imports, package
initializers, schema literals, and schema references; this file contributes
only the semantic roots, non-code extras, and their human-auditable roles.

This is byte and dependency identity for finite local calibration. It grants
no theorem, conceptual-value, physics-value, or external-validation authority.
"""

from __future__ import annotations

import copy
import json
from typing import Any, Mapping

from agentic.discovery.contracts import canonical_json
from agentic.discovery.dependency_authority import (
    DependencyAuthorityError,
    build_dependency_authority,
    validate_dependency_authority,
)


class FormalDependencyAuthorityError(ValueError):
    """Raised when the formal dependency profile is unsafe, incomplete, or stale."""


_RUN_CONTEXT_CONSTRUCTION_KEY = object()


class _FormalDependencyRunContext:
    """Opaque immutable proof that one authority record crossed a full boundary.

    Raw mappings are deliberately not accepted by cached formal hot paths.  The
    only constructors below first build or fully validate the repository-local
    closure, then store canonical bytes so callers cannot mutate nested authority
    rows after validation.  The object remains picklable for isolated workers.
    """

    __slots__ = ("_authority_bytes",)

    def __init__(
        self,
        authority: Mapping[str, Any],
        *,
        _construction_key: object,
    ) -> None:
        if _construction_key is not _RUN_CONTEXT_CONSTRUCTION_KEY:
            raise FormalDependencyAuthorityError(
                "formal dependency run contexts can only be created by an exact boundary"
            )
        self._authority_bytes = canonical_json(copy.deepcopy(dict(authority)))

    def snapshot(self) -> dict[str, Any]:
        """Return a detached copy of the already boundary-validated authority."""

        return json.loads(self._authority_bytes)

    @property
    def content_digest(self) -> str:
        return str(self.snapshot()["content_digest"])


def _build_formal_dependency_run_context() -> _FormalDependencyRunContext:
    """Build one exact authority and wrap it for cache-safe internal reuse."""

    return _FormalDependencyRunContext(
        build_formal_dependency_authority(),
        _construction_key=_RUN_CONTEXT_CONSTRUCTION_KEY,
    )


def _validate_formal_dependency_run_context(
    authority: Mapping[str, Any],
) -> _FormalDependencyRunContext:
    """Fully drift-check an authority before admitting it to cached hot paths."""

    return _FormalDependencyRunContext(
        validate_formal_dependency_authority(authority),
        _construction_key=_RUN_CONTEXT_CONSTRUCTION_KEY,
    )


FORMAL_AUTHORITY_SCOPE = "finite_formal_abstraction_local_closure"
FORMAL_AUTHORITY_BOUNDARY = (
    "Exact repository-local implementation, import, schema, contract, skill, and runtime "
    "identity only; finite structural calibration with no theorem, conceptual-value, "
    "physics-value, or external authority."
)
FORMAL_ENTRY_PYTHON_PATHS: dict[str, tuple[str, ...]] = {
    "skills/common/abstraction_discovery_validation.py": (
        "forge_contract_validator",
        "ym_bridge_validator",
    ),
    "skills/common/abstraction_formal_reasoning.py": (
        "finite_forger",
        "witness_replay",
    ),
    "skills/common/abstraction_parallel_evaluation.py": (
        "blinded_evaluator",
        "condition_runtime",
    ),
    "skills/common/ym_abstraction_calibrations.py": (
        "ym_calibration_registry",
        "ym_calibration_replay",
    ),
    "skills/common/theory_atlas_defect_compiler.py": (
        "theory_atlas_compiler",
        "preserved_source_replay",
        "finite_completion_replay",
    ),
}
FORMAL_SEMANTIC_PATHS: dict[str, tuple[str, ...]] = {
    "agentic/discovery/contracts.py": (
        "canonical_identity_contract",
        "schema_loader",
    ),
    "agentic/discovery/dependency_authority.py": ("dependency_closure_builder",),
    "agentic/registries/skill_quality_registry.yaml": ("skill_quality_contract",),
    "agentic/registries/skill_registry.yaml": ("skill_identity_registry",),
    "skills/common/discovery_lens_heuristic.py": ("lens_projection",),
    "skills/common/formal_dependency_authority.py": ("formal_dependency_profile",),
    "skills/discovery/categorical-concept-forger/SKILL.md": (
        "categorical_skill_contract",
    ),
    "skills/discovery/hott-equivalence-coherence-forger/SKILL.md": (
        "hott_skill_contract",
    ),
    "skills/discovery/theory-atlas-defect-compiler/SKILL.md": (
        "theory_atlas_skill_contract",
    ),
    "skills/yang_mills/ym-categorical-hott-physics-bridge/SKILL.md": (
        "ym_skill_contract",
    ),
    "agentic/external/higher_abductive_theory_discovery/2026-07-22/source_archives/higher_abductive_theory_discovery_system.zip": (
        "preserved_reference_archive",
    ),
    "agentic/external/higher_abductive_theory_discovery/2026-07-22/source_manifest.json": (
        "preserved_reference_manifest",
    ),
    "agentic/external/higher_abductive_theory_discovery/2026-07-22/archive_member_manifest.json": (
        "preserved_reference_member_manifest",
    ),
    "agentic/external/higher_abductive_theory_discovery/2026-07-22/active_index.json": (
        "preserved_reference_active_index",
    ),
    "agentic/external/higher_abductive_theory_discovery/2026-07-22/capability_map.json": (
        "preserved_reference_capability_map",
    ),
    "agentic/external/higher_abductive_theory_discovery/2026-07-22/checksum_report.json": (
        "preserved_reference_checksum_report",
    ),
}
FORMAL_RUNTIME_DISTRIBUTIONS = {
    "jsonschema": "jsonschema",
    "referencing": "referencing",
}


def build_formal_dependency_authority() -> dict[str, Any]:
    """Derive the exact import/schema-complete finite formal authority."""

    try:
        return build_dependency_authority(
            scope=FORMAL_AUTHORITY_SCOPE,
            entry_python_paths=FORMAL_ENTRY_PYTHON_PATHS,
            semantic_paths=FORMAL_SEMANTIC_PATHS,
            authority_boundary=FORMAL_AUTHORITY_BOUNDARY,
            runtime_distributions=FORMAL_RUNTIME_DISTRIBUTIONS,
        )
    except DependencyAuthorityError as exc:
        raise FormalDependencyAuthorityError(str(exc)) from exc


def validate_formal_dependency_authority(
    authority: Mapping[str, Any],
) -> dict[str, Any]:
    """Reject any missing, foreign, mutated, deleted, or newly imported dependency."""

    try:
        return validate_dependency_authority(
            authority,
            scope=FORMAL_AUTHORITY_SCOPE,
            entry_python_paths=FORMAL_ENTRY_PYTHON_PATHS,
            semantic_paths=FORMAL_SEMANTIC_PATHS,
            authority_boundary=FORMAL_AUTHORITY_BOUNDARY,
            runtime_distributions=FORMAL_RUNTIME_DISTRIBUTIONS,
        )
    except DependencyAuthorityError as exc:
        raise FormalDependencyAuthorityError(str(exc)) from exc


__all__ = [
    "FORMAL_AUTHORITY_BOUNDARY",
    "FORMAL_AUTHORITY_SCOPE",
    "FORMAL_ENTRY_PYTHON_PATHS",
    "FORMAL_RUNTIME_DISTRIBUTIONS",
    "FORMAL_SEMANTIC_PATHS",
    "FormalDependencyAuthorityError",
    "build_formal_dependency_authority",
    "validate_formal_dependency_authority",
]
