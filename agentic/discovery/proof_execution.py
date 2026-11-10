# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exact, claim-bound proof execution and total terminal evidence.

The current proof stack has two distinct responsibilities that must not be
blurred:

* a live prelaunch capability performs the one-shot durable claim CAS; and
* an execution layer stages exact bytes and records one total operational
  outcome.

The public executor at the end of this module accepts only the live prelaunch
capability.  It consumes that capability once, derives all runtime material
from the resulting claim and the capability-bound coordination ledger, and
atomically finalizes the resulting evidence before returning.  A
:class:`StagedProofInvocation` remains inert evidence and is never accepted as
launch or retry authority.

All mutable JSON-shaped evidence is retained as private canonical bytes.
Public accessors decode defensive copies.  Source, executable, dependency,
stdin, checker-output, and result-artifact bytes are represented by frozen
attachments whose lengths and SHA-256 digests are recomputed locally.
Operational success remains separate from claim truth, checker soundness,
theoremhood, theory selection, same-cycle mutation, and physics authority.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import os
import platform
import re
import stat
import sys
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Mapping, Sequence

from .budgets import (
    TERMINAL_STATUSES as GOVERNOR_TERMINAL_STATUSES,
    ResourceBudget,
    ResourceGovernor,
    complete_governed_process_environment,
    minimal_replacement_environment,
    validate_v2_process_event,
)
from .contracts import (
    ROOT,
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    safe_relative_path,
    stable_identifier,
    validate_digest,
    validate_identifier,
)
from .dependency_authority import (
    DependencyAuthorityError,
    build_dependency_authority,
    validate_dependency_authority,
)

if TYPE_CHECKING:
    # Runtime importing proof.py here would create a circular authority path.
    # The future public executor may import this type lazily inside its single
    # capability-consuming entrypoint.
    from .proof import ProofPrelaunchCapability


CLAIM_BINDING_CONTRACT_VERSION = "proof-execution-claim-binding/1.0.0"
STAGED_INVOCATION_CONTRACT_VERSION = "proof-execution-invocation/1.0.0"
TERMINAL_RESULT_CONTRACT_VERSION = "proof-execution-terminal/1.0.0"
RUNTIME_REGISTRY_VERSION = "closed-proof-runtime-registry/1.0.0"

MAX_STAGED_FILE_BYTES = 256 * 1024 * 1024
MAX_STAGED_TOTAL_BYTES = 512 * 1024 * 1024
MAX_STAGED_FILES = 512
MAX_STAGED_PATH_BYTES = 1024
MAX_CHECKER_OUTPUT_BYTES = 8 * 1024 * 1024
MAX_ARGV_PARTS = 32
MAX_ARGV_PART_BYTES = 4096

_ROLE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_REASON_CODE = re.compile(r"^[a-z][a-z0-9_]{0,95}$")
_UTC_SECONDS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_CURRENT_WORKER_RELATIVE_PATH = (
    "agentic/scripts/run_discovery_proof_worker_v3.py"
)
_WORKER_RESPONSE_CONTRACT_VERSION = (
    "proof-execution-worker-response/3.0.0"
)

PROOF_EXECUTION_AUTHORITY_NULLS: Mapping[str, bool] = MappingProxyType(
    {
        "truth_authority": False,
        "checker_soundness_authority": False,
        "theorem_authority": False,
        "physics_authority": False,
        "theory_selection_authority": False,
        "same_cycle_theory_mutation": False,
        "serialized_execution_authority": False,
        "cryptographic_authenticity": False,
    }
)

TERMINAL_PROOF_VERDICTS = frozenset(
    {
        "not_evaluated",
        "inconclusive",
        "checker_reported_claim_validated_within_declared_scope",
        "checker_reported_counterexample_validated_within_declared_scope",
        "checker_reported_failed_premise_within_declared_scope",
    }
)

_CHECKER_TO_TERMINAL_VERDICT = {
    "inconclusive": "inconclusive",
    "claim_validated_within_declared_scope": (
        "checker_reported_claim_validated_within_declared_scope"
    ),
    "counterexample_validated_within_declared_scope": (
        "checker_reported_counterexample_validated_within_declared_scope"
    ),
    "failed_premise_validated_within_declared_scope": (
        "checker_reported_failed_premise_within_declared_scope"
    ),
}


class ProofExecutionContractError(ContractError):
    """Reject a detached, mutable, incomplete, or authority-inflating record."""


def _canonical_mapping_bytes(value: Mapping[str, Any], label: str) -> bytes:
    if not isinstance(value, Mapping):
        raise ProofExecutionContractError(f"{label} must be an object")
    try:
        encoded = canonical_json(dict(value))
        decoded = json.loads(encoded)
    except (ContractError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ProofExecutionContractError(
            f"{label} is not canonical JSON: {exc}"
        ) from exc
    if not isinstance(decoded, dict):
        raise ProofExecutionContractError(f"{label} must encode one object")
    return encoded


def _decode_mapping(data: bytes, label: str) -> dict[str, Any]:
    if type(data) is not bytes:
        raise ProofExecutionContractError(f"{label} bytes must be exact bytes")
    try:
        value = json.loads(data)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ProofExecutionContractError(
            f"{label} bytes are not canonical JSON"
        ) from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise ProofExecutionContractError(
            f"{label} bytes do not encode one canonical object"
        )
    return value


def _self_digest(value: Mapping[str, Any], field: str = "content_digest") -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def _require_self_digest(
    value: Mapping[str, Any],
    *,
    label: str,
    field: str = "content_digest",
) -> None:
    supplied = value.get(field)
    try:
        validate_digest(supplied)
    except ContractError as exc:
        raise ProofExecutionContractError(
            f"{label} has an invalid {field}"
        ) from exc
    if supplied != _self_digest(value, field):
        raise ProofExecutionContractError(f"{label} {field} mismatch")


def _require_exact_keys(
    value: Mapping[str, Any], expected: frozenset[str], label: str
) -> None:
    actual = frozenset(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ProofExecutionContractError(
            f"{label} shape differs: missing={missing}, extra={extra}"
        )


def _validated_utc_seconds(value: str, label: str) -> dt.datetime:
    if not isinstance(value, str) or not _UTC_SECONDS.fullmatch(value):
        raise ProofExecutionContractError(
            f"{label} must be second-resolution UTC ending in Z"
        )
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProofExecutionContractError(f"{label} is not a valid instant") from exc
    return parsed.astimezone(dt.UTC)


def _validated_utc_instant(value: str, label: str) -> dt.datetime:
    """Validate a canonical UTC instant while allowing recorded microseconds."""

    if not isinstance(value, str) or not value.endswith("Z"):
        raise ProofExecutionContractError(f"{label} must be a UTC instant ending in Z")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProofExecutionContractError(f"{label} is not a valid instant") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != dt.timedelta(0):
        raise ProofExecutionContractError(f"{label} must be canonical UTC")
    return parsed.astimezone(dt.UTC)


def _utc_now_seconds() -> str:
    return (
        dt.datetime.now(dt.UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _validated_reason_code(value: str) -> str:
    if not isinstance(value, str) or not _REASON_CODE.fullmatch(value):
        raise ProofExecutionContractError(
            "terminal reason_code must be one lower-snake-case token"
        )
    return value


def _validated_relative_path(raw: str, label: str) -> str:
    if (
        not isinstance(raw, str)
        or len(raw.encode("utf-8")) > MAX_STAGED_PATH_BYTES
    ):
        raise ProofExecutionContractError(
            f"{label} exceeds the fixed path-byte ceiling"
        )
    try:
        normalized = safe_relative_path(raw, forbid_latest=True).as_posix()
    except ContractError as exc:
        raise ProofExecutionContractError(f"{label} is unsafe") from exc
    if normalized != raw or "\\" in raw:
        raise ProofExecutionContractError(f"{label} is not canonical POSIX")
    return normalized


def _validate_authority_nulls(value: Any, label: str) -> dict[str, bool]:
    expected = dict(PROOF_EXECUTION_AUTHORITY_NULLS)
    if not isinstance(value, Mapping) or dict(value) != expected:
        raise ProofExecutionContractError(
            f"{label} must preserve every proof authority null"
        )
    return expected


def _validate_argv(value: Sequence[str]) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ProofExecutionContractError("logical argv must be a string sequence")
    result = tuple(value)
    if not result or len(result) > MAX_ARGV_PARTS:
        raise ProofExecutionContractError("logical argv cardinality is invalid")
    if any(
        not isinstance(part, str)
        or not part
        or "\x00" in part
        or len(part.encode("utf-8")) > MAX_ARGV_PART_BYTES
        for part in result
    ):
        raise ProofExecutionContractError(
            "logical argv contains an empty, NUL, non-string, or oversized part"
        )
    return result


@dataclasses.dataclass(frozen=True, slots=True)
class ProofRuntimeRoute:
    """One route row in the closed proof-runtime registry.

    ``logical_entrypoint`` is deliberately a registry token, not an ambient
    executable path.  Built-in rows can launch only after the current executor
    binds the token to exact staged interpreter and worker bytes.  Lean and
    external rows remain explicitly unavailable.
    """

    adapter: str
    route_id: str
    logical_entrypoint: str
    request_protocol: str
    response_protocol: str
    source_policy: str
    artifact_policy: str

    def __post_init__(self) -> None:
        if self.adapter not in {"exact", "finite_model", "lean", "external"}:
            raise ProofExecutionContractError("proof runtime adapter is unregistered")
        validate_identifier(self.route_id, "proof runtime route_id")
        if self.logical_entrypoint != f"registry://proof/{self.adapter}/v1":
            raise ProofExecutionContractError(
                "proof runtime logical entrypoint is not registry-derived"
            )
        if not self.request_protocol or not self.response_protocol:
            raise ProofExecutionContractError(
                "proof runtime protocols must be explicit"
            )
        if self.source_policy not in {"forbidden", "required_exact_lean_source"}:
            raise ProofExecutionContractError("proof runtime source policy is invalid")
        if self.artifact_policy not in {
            "forbidden",
            "required_fresh_regular_file",
            "execution_plan_bound",
        }:
            raise ProofExecutionContractError(
                "proof runtime artifact policy is invalid"
            )

    def projection(self) -> dict[str, Any]:
        launch_implemented = self.adapter in {"exact", "finite_model"}
        row: dict[str, Any] = {
            "registry_version": RUNTIME_REGISTRY_VERSION,
            "adapter": self.adapter,
            "route_id": self.route_id,
            "logical_entrypoint": self.logical_entrypoint,
            "request_protocol": self.request_protocol,
            "response_protocol": self.response_protocol,
            "source_policy": self.source_policy,
            "artifact_policy": self.artifact_policy,
            "worker_role": "solver",
            "launch_implemented": launch_implemented,
            "ambient_path_resolution_allowed": False,
            "authority_nulls": dict(PROOF_EXECUTION_AUTHORITY_NULLS),
        }
        row["content_digest"] = _self_digest(row)
        return row


_RUNTIME_ROUTES = (
    ProofRuntimeRoute(
        adapter="exact",
        route_id="proof-runtime-exact-v1",
        logical_entrypoint="registry://proof/exact/v1",
        request_protocol="proof-execution-request/1.0.0",
        response_protocol="builtin-exact-response/1.0.0",
        source_policy="forbidden",
        artifact_policy="forbidden",
    ),
    ProofRuntimeRoute(
        adapter="finite_model",
        route_id="proof-runtime-finite-model-v1",
        logical_entrypoint="registry://proof/finite_model/v1",
        request_protocol="proof-execution-request/1.0.0",
        response_protocol="builtin-finite-model-response/1.0.0",
        source_policy="forbidden",
        artifact_policy="forbidden",
    ),
    ProofRuntimeRoute(
        adapter="lean",
        route_id="proof-runtime-lean-v1",
        logical_entrypoint="registry://proof/lean/v1",
        request_protocol="proof-execution-request/1.0.0",
        response_protocol="lean-kernel-evidence/1.0.0",
        source_policy="required_exact_lean_source",
        artifact_policy="required_fresh_regular_file",
    ),
    ProofRuntimeRoute(
        adapter="external",
        route_id="proof-runtime-external-v1",
        logical_entrypoint="registry://proof/external/v1",
        request_protocol="proof-execution-request/1.0.0",
        response_protocol="external-checker-response/1.0.0",
        source_policy="forbidden",
        artifact_policy="execution_plan_bound",
    ),
)
_RUNTIME_ROUTE_BY_ADAPTER = MappingProxyType(
    {route.adapter: route for route in _RUNTIME_ROUTES}
)


def resolve_proof_runtime_route(adapter: str) -> ProofRuntimeRoute:
    """Resolve one adapter without accepting a caller-provided command."""

    normalized = "external" if adapter == "command" else adapter
    try:
        return _RUNTIME_ROUTE_BY_ADAPTER[normalized]
    except (KeyError, TypeError) as exc:
        raise ProofExecutionContractError(
            f"proof adapter has no closed runtime route: {adapter!r}"
        ) from exc


def closed_proof_runtime_registry() -> tuple[dict[str, Any], ...]:
    """Return defensive inert projections of every registered route."""

    return tuple(route.projection() for route in _RUNTIME_ROUTES)


def _normalize_profile_rows(
    raw: Mapping[str, Sequence[str]], label: str
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    if not isinstance(raw, Mapping) or not raw:
        raise ProofExecutionContractError(f"{label} must be a non-empty mapping")
    rows: list[tuple[str, tuple[str, ...]]] = []
    for raw_path, raw_roles in sorted(raw.items()):
        path = _validated_relative_path(raw_path, f"{label} path")
        if isinstance(raw_roles, (str, bytes)) or not isinstance(
            raw_roles, Sequence
        ):
            raise ProofExecutionContractError(f"{label} roles must be a sequence")
        roles = tuple(sorted(set(raw_roles)))
        if (
            not roles
            or any(not isinstance(role, str) or not _ROLE.fullmatch(role) for role in roles)
        ):
            raise ProofExecutionContractError(f"{label} roles are invalid")
        rows.append((path, roles))
    return tuple(rows)


@dataclasses.dataclass(frozen=True, slots=True)
class ProofDependencyProfile:
    """Frozen inputs for the repository dependency-authority derivation."""

    scope: str
    entry_python_rows: tuple[tuple[str, tuple[str, ...]], ...]
    semantic_rows: tuple[tuple[str, tuple[str, ...]], ...]
    authority_boundary: str
    runtime_distribution_rows: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.scope, str) or not self.scope.strip():
            raise ProofExecutionContractError("dependency scope is required")
        if (
            not isinstance(self.authority_boundary, str)
            or len(self.authority_boundary.strip()) < 8
        ):
            raise ProofExecutionContractError(
                "dependency authority boundary is not substantive"
            )
        if tuple(sorted(self.entry_python_rows)) != self.entry_python_rows:
            raise ProofExecutionContractError(
                "entry Python dependency rows are not canonical"
            )
        if tuple(sorted(self.semantic_rows)) != self.semantic_rows:
            raise ProofExecutionContractError(
                "semantic dependency rows are not canonical"
            )
        for label, rows in (
            ("entry Python", self.entry_python_rows),
            ("semantic", self.semantic_rows),
        ):
            if not rows:
                raise ProofExecutionContractError(
                    f"{label} dependency rows cannot be empty"
                )
            for path, roles in rows:
                _validated_relative_path(path, f"{label} dependency path")
                if (
                    tuple(sorted(set(roles))) != roles
                    or not roles
                    or any(not _ROLE.fullmatch(role) for role in roles)
                ):
                    raise ProofExecutionContractError(
                        f"{label} dependency roles are invalid"
                    )
        if tuple(sorted(self.runtime_distribution_rows)) != (
            self.runtime_distribution_rows
        ):
            raise ProofExecutionContractError(
                "runtime distribution rows are not canonical"
            )
        if any(
            not module.isidentifier() or not distribution.strip()
            for module, distribution in self.runtime_distribution_rows
        ):
            raise ProofExecutionContractError(
                "runtime distribution rows are invalid"
            )

    @classmethod
    def from_mappings(
        cls,
        *,
        scope: str,
        entry_python_paths: Mapping[str, Sequence[str]],
        semantic_paths: Mapping[str, Sequence[str]],
        authority_boundary: str,
        runtime_distributions: Mapping[str, str] | None = None,
    ) -> "ProofDependencyProfile":
        """Freeze one exact dependency profile without touching the filesystem."""

        distribution_rows = tuple(
            sorted(
                (str(module), str(distribution))
                for module, distribution in (runtime_distributions or {}).items()
            )
        )
        return cls(
            scope=scope,
            entry_python_rows=_normalize_profile_rows(
                entry_python_paths, "entry_python_paths"
            ),
            semantic_rows=_normalize_profile_rows(
                semantic_paths, "semantic_paths"
            ),
            authority_boundary=authority_boundary,
            runtime_distribution_rows=distribution_rows,
        )

    def _entry_mapping(self) -> dict[str, tuple[str, ...]]:
        return dict(self.entry_python_rows)

    def _semantic_mapping(self) -> dict[str, tuple[str, ...]]:
        return dict(self.semantic_rows)

    def _distribution_mapping(self) -> dict[str, str]:
        return dict(self.runtime_distribution_rows)

    def build_authority(
        self, *, repository_root: Path | str = ROOT
    ) -> dict[str, Any]:
        """Derive the complete local Python/schema closure for this profile."""

        try:
            return build_dependency_authority(
                scope=self.scope,
                entry_python_paths=self._entry_mapping(),
                semantic_paths=self._semantic_mapping(),
                authority_boundary=self.authority_boundary,
                repository_root=repository_root,
                runtime_distributions=self._distribution_mapping(),
            )
        except DependencyAuthorityError as exc:
            raise ProofExecutionContractError(
                f"proof dependency authority cannot be built: {exc}"
            ) from exc

    def validate_authority(
        self,
        record: Mapping[str, Any],
        *,
        repository_root: Path | str = ROOT,
    ) -> dict[str, Any]:
        """Recompute and reject graph, byte, schema, or runtime drift."""

        try:
            return validate_dependency_authority(
                record,
                scope=self.scope,
                entry_python_paths=self._entry_mapping(),
                semantic_paths=self._semantic_mapping(),
                authority_boundary=self.authority_boundary,
                repository_root=repository_root,
                runtime_distributions=self._distribution_mapping(),
            )
        except DependencyAuthorityError as exc:
            raise ProofExecutionContractError(
                f"proof dependency authority is stale or incomplete: {exc}"
            ) from exc


@dataclasses.dataclass(frozen=True, slots=True)
class StagedByteArtifact:
    """Exact immutable bytes assigned one or more execution-stage roles."""

    relative_path: str
    content: bytes = dataclasses.field(repr=False)
    roles: tuple[str, ...]
    executable: bool = False
    content_digest: str = dataclasses.field(init=False)
    byte_length: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        _validated_relative_path(self.relative_path, "staged artifact path")
        if type(self.content) is not bytes:
            raise ProofExecutionContractError(
                "staged artifact content must be exact immutable bytes"
            )
        if len(self.content) > MAX_STAGED_FILE_BYTES:
            raise ProofExecutionContractError("staged artifact exceeds its byte ceiling")
        if (
            type(self.roles) is not tuple
            or not self.roles
            or tuple(sorted(set(self.roles))) != self.roles
            or any(not isinstance(role, str) or not _ROLE.fullmatch(role) for role in self.roles)
        ):
            raise ProofExecutionContractError(
                "staged artifact roles must be canonical and non-empty"
            )
        if type(self.executable) is not bool:
            raise ProofExecutionContractError("staged executable flag must be boolean")
        if self.executable != ("executable" in self.roles):
            raise ProofExecutionContractError(
                "staged executable flag and executable role differ"
            )
        object.__setattr__(self, "content_digest", bytes_digest(self.content))
        object.__setattr__(self, "byte_length", len(self.content))

    @classmethod
    def from_bytes(
        cls,
        relative_path: str,
        content: bytes,
        *,
        roles: Sequence[str],
        executable: bool = False,
    ) -> "StagedByteArtifact":
        """Copy exact bytes into a canonical frozen attachment."""

        if type(content) is not bytes:
            raise ProofExecutionContractError(
                "staged artifact input must be exact bytes"
            )
        normalized_roles = set(roles)
        if executable:
            normalized_roles.add("executable")
        return cls(
            relative_path=_validated_relative_path(
                relative_path, "staged artifact path"
            ),
            content=memoryview(content).tobytes(),
            roles=tuple(sorted(normalized_roles)),
            executable=executable,
        )

    def descriptor(self) -> dict[str, Any]:
        """Return the content-addressed projection; bytes remain attached."""

        return {
            "relative_path": self.relative_path,
            "roles": list(self.roles),
            "sha256": self.content_digest,
            "byte_length": self.byte_length,
            "executable": self.executable,
        }

    def read_bytes(self) -> bytes:
        """Return a fresh immutable copy for a later private stager."""

        return memoryview(self.content).tobytes()


def _validate_dependency_authority_projection(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    payload = _decode_mapping(
        _canonical_mapping_bytes(record, "dependency authority"),
        "dependency authority",
    )
    required = {
        "authority_version",
        "scope",
        "declared_roots",
        "entries",
        "schema_closure",
        "import_boundary",
        "runtime_dependencies",
        "authority_boundary",
        "content_digest",
    }
    if not required.issubset(payload):
        raise ProofExecutionContractError(
            "dependency authority lacks its closed-graph fields"
        )
    _require_self_digest(payload, label="dependency authority")
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ProofExecutionContractError(
            "dependency authority must contain at least one entry"
        )
    prior_path = ""
    for row in entries:
        if not isinstance(row, Mapping):
            raise ProofExecutionContractError(
                "dependency authority entry must be an object"
            )
        _require_exact_keys(
            row,
            frozenset({"path", "roles", "byte_size", "content_digest"}),
            "dependency authority entry",
        )
        path = _validated_relative_path(row["path"], "dependency entry path")
        if path <= prior_path:
            raise ProofExecutionContractError(
                "dependency authority entries are not strictly path-sorted"
            )
        prior_path = path
        roles = row["roles"]
        if (
            not isinstance(roles, list)
            or not roles
            or roles != sorted(set(roles))
            or any(not isinstance(role, str) or not _ROLE.fullmatch(role) for role in roles)
        ):
            raise ProofExecutionContractError(
                "dependency authority entry roles are invalid"
            )
        size = row["byte_size"]
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise ProofExecutionContractError(
                "dependency authority entry byte_size is invalid"
            )
        try:
            validate_digest(row["content_digest"])
        except ContractError as exc:
            raise ProofExecutionContractError(
                "dependency authority entry digest is invalid"
            ) from exc
    return payload


def _validate_executable_authority_projection(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate the exact interpreter-byte authority and its honest remainder."""

    payload = _decode_mapping(
        _canonical_mapping_bytes(record, "proof executable authority"),
        "proof executable authority",
    )
    _require_exact_keys(
        payload,
        frozenset(
            {
                "authority_version",
                "authority_kind",
                "source_path",
                "staged_relative_path",
                "sha256",
                "byte_length",
                "source_mode",
                "source_device",
                "source_inode",
                "source_mtime_ns",
                "python_version",
                "python_implementation",
                "platform_system",
                "platform_machine",
                "stdlib_byte_closure_complete",
                "shared_library_byte_closure_complete",
                "host_runtime_closure_status",
                "ambient_path_resolution_allowed",
                "authority_boundary",
                "content_digest",
            }
        ),
        "proof executable authority",
    )
    _require_self_digest(payload, label="proof executable authority")
    source = Path(str(payload["source_path"]))
    if (
        payload["authority_version"] != "1.0.0"
        or payload["authority_kind"] != "current_process_python_executable_bytes"
        or not source.is_absolute()
        or source.as_posix() != payload["source_path"]
        or payload["staged_relative_path"] != "executables/python"
        or isinstance(payload["byte_length"], bool)
        or not isinstance(payload["byte_length"], int)
        or payload["byte_length"] <= 0
        or any(
            isinstance(payload[field], bool)
            or not isinstance(payload[field], int)
            or payload[field] < 0
            for field in (
                "source_mode",
                "source_device",
                "source_inode",
                "source_mtime_ns",
            )
        )
        or payload["stdlib_byte_closure_complete"] is not False
        or payload["shared_library_byte_closure_complete"] is not False
        or payload["host_runtime_closure_status"] != "unavailable_unhashed_remainder"
        or payload["ambient_path_resolution_allowed"] is not False
        or not isinstance(payload["authority_boundary"], str)
        or len(payload["authority_boundary"]) < 16
    ):
        raise ProofExecutionContractError(
            "proof executable authority is incomplete or overstates host closure"
        )
    try:
        validate_digest(payload["sha256"])
    except ContractError as exc:
        raise ProofExecutionContractError(
            "proof executable authority digest is invalid"
        ) from exc
    for field in (
        "python_version",
        "python_implementation",
        "platform_system",
        "platform_machine",
    ):
        if not isinstance(payload[field], str) or not payload[field]:
            raise ProofExecutionContractError(
                "proof executable runtime identity is incomplete"
            )
    return payload


def _safe_regular_file_bytes(root: Path, relative: str) -> tuple[bytes, os.stat_result]:
    """Capture one regular file without following an in-root symlink edge."""

    cursor = root
    for part in Path(relative).parts:
        cursor = cursor / part
        metadata = os.lstat(cursor)
        if stat.S_ISLNK(metadata.st_mode):
            raise ProofExecutionContractError(
                f"dependency path traverses a symlink: {relative}"
            )
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(cursor, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ProofExecutionContractError(
                f"dependency is not a regular file: {relative}"
            )
        if before.st_size > MAX_STAGED_FILE_BYTES:
            raise ProofExecutionContractError(
                f"dependency exceeds the staged-file ceiling: {relative}"
            )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                raise ProofExecutionContractError(
                    f"dependency ended before its stated size: {relative}"
                )
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise ProofExecutionContractError(
                f"dependency grew while it was captured: {relative}"
            )
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    stable_before = (
        before.st_dev,
        before.st_ino,
        before.st_mode,
        before.st_nlink,
        before.st_size,
        before.st_mtime_ns,
    )
    stable_after = (
        after.st_dev,
        after.st_ino,
        after.st_mode,
        after.st_nlink,
        after.st_size,
        after.st_mtime_ns,
    )
    if stable_before != stable_after:
        raise ProofExecutionContractError(
            f"dependency changed while it was captured: {relative}"
        )
    return b"".join(chunks), after


def capture_dependency_artifacts(
    profile: ProofDependencyProfile,
    authority: Mapping[str, Any],
    *,
    repository_root: Path | str = ROOT,
) -> tuple[StagedByteArtifact, ...]:
    """Capture every authority entry as immutable bytes and replay its digest."""

    expected = profile.validate_authority(
        authority, repository_root=repository_root
    )
    payload = _validate_dependency_authority_projection(expected)
    root = Path(repository_root)
    if root.is_symlink() or not root.is_dir():
        raise ProofExecutionContractError(
            "dependency repository root must be a non-symlink directory"
        )
    root = root.resolve(strict=True)
    artifacts: list[StagedByteArtifact] = []
    total = 0
    for row in payload["entries"]:
        content, metadata = _safe_regular_file_bytes(root, row["path"])
        if (
            len(content) != row["byte_size"]
            or bytes_digest(content) != row["content_digest"]
        ):
            raise ProofExecutionContractError(
                f"captured dependency bytes differ from authority: {row['path']}"
            )
        total += len(content)
        if total > MAX_STAGED_TOTAL_BYTES:
            raise ProofExecutionContractError(
                "captured dependencies exceed the total byte ceiling"
            )
        executable = bool(metadata.st_mode & 0o111)
        roles = {"dependency", *row["roles"]}
        artifacts.append(
            StagedByteArtifact.from_bytes(
                row["path"],
                content,
                roles=tuple(sorted(roles)),
                executable=executable,
            )
        )
    return tuple(artifacts)


@dataclasses.dataclass(frozen=True, slots=True)
class ProofExecutionClaimBinding:
    """Inert exact evidence returned after the durable prelaunch CAS.

    This record is deliberately reconstructible from verified mappings because
    it is evidence, not a live launch token.  Future launch code must never
    accept it in place of :class:`ProofPrelaunchCapability`.
    """

    _prelaunch_projection_bytes: bytes = dataclasses.field(repr=False)
    _handoff_bytes: bytes = dataclasses.field(repr=False)
    _reservation_bytes: bytes = dataclasses.field(repr=False)
    _execution_claim_bytes: bytes = dataclasses.field(repr=False)
    _execution_claim_reference_bytes: bytes = dataclasses.field(repr=False)
    _projection_bytes: bytes = dataclasses.field(init=False, repr=False)
    _resource_budget: ResourceBudget = dataclasses.field(init=False, repr=False)

    def __post_init__(self) -> None:
        for label, data in (
            ("prelaunch projection", self._prelaunch_projection_bytes),
            ("proof handoff", self._handoff_bytes),
            ("proof reservation", self._reservation_bytes),
            ("proof execution claim", self._execution_claim_bytes),
            ("proof execution claim reference", self._execution_claim_reference_bytes),
        ):
            if type(data) is not bytes:
                raise ProofExecutionContractError(
                    f"{label} must be retained as exact canonical bytes"
                )
        projection, budget = _claim_binding_projection(self)
        object.__setattr__(self, "_projection_bytes", canonical_json(projection))
        object.__setattr__(self, "_resource_budget", budget)

    @classmethod
    def from_consumed_records(
        cls,
        *,
        prelaunch_projection: Mapping[str, Any],
        handoff: Mapping[str, Any],
        reservation: Mapping[str, Any],
        execution_claim: Mapping[str, Any],
        execution_claim_reference: Mapping[str, Any],
    ) -> "ProofExecutionClaimBinding":
        """Bind verified post-CAS records without granting launch authority."""

        return cls(
            _prelaunch_projection_bytes=_canonical_mapping_bytes(
                prelaunch_projection, "prelaunch projection"
            ),
            _handoff_bytes=_canonical_mapping_bytes(handoff, "proof handoff"),
            _reservation_bytes=_canonical_mapping_bytes(
                reservation, "proof reservation"
            ),
            _execution_claim_bytes=_canonical_mapping_bytes(
                execution_claim, "proof execution claim"
            ),
            _execution_claim_reference_bytes=_canonical_mapping_bytes(
                execution_claim_reference, "proof execution claim reference"
            ),
        )

    @property
    def prelaunch_projection(self) -> Mapping[str, Any]:
        return _decode_mapping(
            self._prelaunch_projection_bytes, "prelaunch projection"
        )

    @property
    def handoff(self) -> Mapping[str, Any]:
        return _decode_mapping(self._handoff_bytes, "proof handoff")

    @property
    def reservation(self) -> Mapping[str, Any]:
        return _decode_mapping(self._reservation_bytes, "proof reservation")

    @property
    def execution_claim(self) -> Mapping[str, Any]:
        return _decode_mapping(
            self._execution_claim_bytes, "proof execution claim"
        )

    @property
    def execution_claim_reference(self) -> Mapping[str, Any]:
        return _decode_mapping(
            self._execution_claim_reference_bytes,
            "proof execution claim reference",
        )

    @property
    def resource_budget(self) -> ResourceBudget:
        return self._resource_budget

    @property
    def projection(self) -> Mapping[str, Any]:
        return _decode_mapping(self._projection_bytes, "proof claim binding")


def _claim_binding_projection(
    binding: ProofExecutionClaimBinding,
) -> tuple[dict[str, Any], ResourceBudget]:
    prelaunch = _decode_mapping(
        binding._prelaunch_projection_bytes, "prelaunch projection"
    )
    handoff = _decode_mapping(binding._handoff_bytes, "proof handoff")
    reservation = _decode_mapping(binding._reservation_bytes, "proof reservation")
    claim = _decode_mapping(
        binding._execution_claim_bytes, "proof execution claim"
    )
    claim_reference = _decode_mapping(
        binding._execution_claim_reference_bytes,
        "proof execution claim reference",
    )

    _require_self_digest(prelaunch, label="prelaunch projection")
    _require_self_digest(handoff, label="proof handoff")
    _require_self_digest(
        reservation, label="proof reservation", field="reservation_digest"
    )
    _require_self_digest(
        claim, label="proof execution claim", field="execution_claim_digest"
    )
    _require_self_digest(
        claim_reference,
        label="proof execution claim reference",
        field="reference_digest",
    )
    if (
        prelaunch.get("schema_version") != 3
        or prelaunch.get("capability_kind")
        != "one_shot_unclaimed_postcommit_proof_prelaunch"
        or prelaunch.get("projection_phase") != "before_durable_execution_claim"
        or prelaunch.get("durable_claim_present_in_projection") is not False
        or prelaunch.get("projection_only") is not True
        or prelaunch.get("authoritative_for_execution") is not False
        or prelaunch.get("live_capability_required") is not True
        or prelaunch.get("one_shot") is not True
        or prelaunch.get("serialized_reconstruction_allowed") is not False
    ):
        raise ProofExecutionContractError(
            "prelaunch projection does not preserve its inert one-shot boundary"
        )
    if (
        handoff.get("schema_version") != 3
        or handoff.get("projection_only") is not True
        or handoff.get("postcommit_reopen_required") is not True
    ):
        raise ProofExecutionContractError(
            "proof handoff is not one inert current v3 projection"
        )
    _validate_authority_nulls(handoff.get("authority_nulls"), "proof handoff")
    if (
        reservation.get("record_kind") != "proof_attempt_reservation"
        or claim.get("record_kind") != "proof_execution_claim"
        or claim.get("status") != "proof_execution_claimed"
    ):
        raise ProofExecutionContractError(
            "consumed proof records have the wrong lifecycle kinds"
        )

    direct_fields = (
        "target_id",
        "run_id",
        "handoff_id",
        "attempt_id",
        "attempt_number",
        "reservation_id",
        "reservation_digest",
        "execution_claim_id",
        "action_id",
        "action_digest",
    )
    for field in direct_fields:
        available = [
            value[field]
            for value in (prelaunch, reservation, claim)
            if field in value
        ]
        if len(available) < 2 or any(item != available[0] for item in available[1:]):
            raise ProofExecutionContractError(
                f"proof claim records disagree on {field}"
            )
    handoff_pairs = {
        "handoff_id": "handoff_id",
        "handoff_digest": "content_digest",
        "target_id": "target_id",
        "run_id": "run_id",
        "cycle_id": "cycle_id",
        "branch_id": "branch_id",
        "execution_plan_digest": "execution_plan_digest",
        "proof_adapter": "proof_adapter",
        "literature_consume_before": "literature_consume_before",
    }
    for prelaunch_field, handoff_field in handoff_pairs.items():
        if prelaunch.get(prelaunch_field) != handoff.get(handoff_field):
            raise ProofExecutionContractError(
                f"prelaunch projection crossed proof handoff field {handoff_field}"
            )
    if (
        prelaunch.get("action_id") != handoff.get("scheduled_action_id")
        or prelaunch.get("action_digest")
        != handoff.get("scheduled_action_digest")
        or claim.get("handoff_digest") != handoff.get("content_digest")
        or reservation.get("handoff_digest") != handoff.get("content_digest")
    ):
        raise ProofExecutionContractError(
            "proof claim records crossed their scheduled handoff"
        )
    if prelaunch.get("capability_id") is None:
        raise ProofExecutionContractError("prelaunch projection lacks capability_id")
    for field in (
        "target_id",
        "run_id",
        "cycle_id",
        "branch_id",
        "handoff_id",
        "attempt_id",
        "reservation_id",
        "execution_claim_id",
        "action_id",
        "obligation_id",
    ):
        validate_identifier(prelaunch[field], field)
    runtime_ref = _validated_relative_path(
        str(prelaunch.get("proof_runtime_ref")), "proof runtime reference"
    )

    source_recheck = claim.get("source_theory_head_recheck")
    deadline_revalidation = claim.get("deadline_revalidation")
    executor_lease = claim.get("executor_lease")
    if (
        not isinstance(source_recheck, Mapping)
        or source_recheck.get("match") is not True
        or source_recheck.get("expected_head")
        != source_recheck.get("observed_head")
        or source_recheck.get("recheck_digest")
        != _self_digest(source_recheck, "recheck_digest")
        or not isinstance(deadline_revalidation, Mapping)
        or deadline_revalidation.get("revalidation_kind")
        != "governed_deadline_revalidated_at_prelaunch"
        or deadline_revalidation.get("theory_authorization_digest")
        != handoff.get("theory_authorization_digest")
        or deadline_revalidation.get("live_capability_revalidated") is not True
        or deadline_revalidation.get("consume_before")
        != prelaunch.get("literature_consume_before")
        or deadline_revalidation.get("cross_store_atomicity_claimed") is not False
        or deadline_revalidation.get("revalidation_digest")
        != _self_digest(deadline_revalidation, "revalidation_digest")
    ):
        raise ProofExecutionContractError(
            "proof execution claim lacks exact head/deadline revalidation"
        )
    evaluated_at = _validated_utc_instant(
        str(deadline_revalidation.get("evaluated_at")),
        "proof execution deadline evaluated_at",
    )
    consume_before = _validated_utc_instant(
        str(deadline_revalidation.get("consume_before")),
        "proof execution deadline consume_before",
    )
    clock_authority = deadline_revalidation.get("clock_authority")
    if (
        evaluated_at > consume_before
        or not isinstance(clock_authority, Mapping)
        or deadline_revalidation.get("clock_authority_digest")
        != clock_authority.get("authority_digest")
    ):
        raise ProofExecutionContractError(
            "proof execution claim deadline clock evidence is inconsistent"
        )
    if (
        not isinstance(executor_lease, Mapping)
        or executor_lease.get("lease_kind")
        != "bounded_single_executor_recovery_lease"
        or executor_lease.get("reservation_id")
        != reservation.get("reservation_id")
        or executor_lease.get("reservation_digest")
        != reservation.get("reservation_digest")
        or executor_lease.get("execution_claim_id")
        != claim.get("execution_claim_id")
        or executor_lease.get("attempt_id") != reservation.get("attempt_id")
        or executor_lease.get("issued_at")
        != deadline_revalidation.get("evaluated_at")
        or executor_lease.get("lease_digest")
        != _self_digest(executor_lease, "lease_digest")
        or executor_lease.get("bounded") is not True
        or executor_lease.get("renewable") is not False
        or executor_lease.get(
            "launch_boundary_checkpoint_required_before_spawn"
        )
        is not True
        or executor_lease.get("expiry_authorizes_respawn") is not False
        or executor_lease.get("pid_only_death_authority") is not False
        or executor_lease.get("caller_supplied_time_allowed") is not False
    ):
        raise ProofExecutionContractError(
            "proof execution claim lacks its exact bounded executor lease"
        )
    lease_issued = _validated_utc_instant(
        str(executor_lease.get("issued_at")),
        "proof executor lease issued_at",
    )
    lease_expires = _validated_utc_instant(
        str(executor_lease.get("expires_at")),
        "proof executor lease expires_at",
    )
    if lease_expires <= lease_issued:
        raise ProofExecutionContractError(
            "proof executor lease does not have a positive interval"
        )
    observed_head = source_recheck["observed_head"]
    if (
        not isinstance(observed_head, Mapping)
        or observed_head.get("head_digest")
        != prelaunch.get("source_theory_head_digest")
    ):
        raise ProofExecutionContractError(
            "proof execution claim crossed its source theory head"
        )

    record_artifact = claim_reference.get("record_artifact")
    if (
        claim_reference.get("target_id") != prelaunch["target_id"]
        or claim_reference.get("run_id") != prelaunch["run_id"]
        or not isinstance(record_artifact, Mapping)
        or record_artifact.get("sha256")
        != bytes_digest(binding._execution_claim_bytes)
        or record_artifact.get("size_bytes")
        != len(binding._execution_claim_bytes)
    ):
        raise ProofExecutionContractError(
            "proof execution claim reference does not bind the exact claim bytes"
        )

    formal_claim = handoff.get("formal_claim")
    execution_plan = handoff.get("execution_plan")
    resource_budget_raw = handoff.get("resource_budget")
    execution_policy = handoff.get("execution_policy")
    runtime_contract = handoff.get("runtime_contract")
    if not all(
        isinstance(value, Mapping)
        for value in (
            formal_claim,
            execution_plan,
            resource_budget_raw,
            execution_policy,
            runtime_contract,
        )
    ):
        raise ProofExecutionContractError(
            "proof handoff lacks claim, plan, budget, policy, or runtime contract"
        )
    if canonical_digest(formal_claim) != handoff.get("formal_claim_digest"):
        raise ProofExecutionContractError("proof handoff formal claim digest mismatch")
    if canonical_digest(execution_plan) != handoff.get("execution_plan_digest"):
        raise ProofExecutionContractError("proof handoff execution plan digest mismatch")
    try:
        budget = ResourceBudget.from_mapping(resource_budget_raw)
    except (TypeError, ValueError) as exc:
        raise ProofExecutionContractError(
            f"proof handoff resource budget is invalid: {exc}"
        ) from exc
    budget_projection = dataclasses.asdict(budget)
    if budget_projection != dict(resource_budget_raw):
        raise ProofExecutionContractError(
            "proof handoff resource budget is not the exact ResourceBudget projection"
        )
    resource_budget_digest = canonical_digest(budget_projection)
    if (
        resource_budget_digest != prelaunch.get("resource_budget_digest")
        or resource_budget_digest != reservation.get("resource_budget_digest")
    ):
        raise ProofExecutionContractError(
            "proof claim records crossed their resource budget"
        )
    required_policy_keys = {
        "replacement_environment_policy",
        "input_limit_bytes",
        "stdout_limit_bytes",
        "stderr_limit_bytes",
        "filesystem_isolation",
        "network_isolation",
        "trusted_local_worker_required",
    }
    if set(execution_policy) != required_policy_keys:
        raise ProofExecutionContractError(
            "proof execution policy shape is not closed"
        )
    for field in ("input_limit_bytes", "stdout_limit_bytes", "stderr_limit_bytes"):
        limit = execution_policy[field]
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ProofExecutionContractError(
                f"proof execution policy {field} is invalid"
            )
    if execution_policy.get("trusted_local_worker_required") is not True:
        raise ProofExecutionContractError(
            "proof execution policy must require a trusted local worker"
        )

    projection: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": CLAIM_BINDING_CONTRACT_VERSION,
        "binding_kind": "consumed_one_shot_proof_execution_claim_evidence",
        "capability_id": prelaunch["capability_id"],
        "capability_projection_digest": prelaunch["content_digest"],
        "execution_claim_id": claim["execution_claim_id"],
        "execution_claim_digest": claim["execution_claim_digest"],
        "execution_claim_reference_digest": claim_reference["reference_digest"],
        "reservation_id": reservation["reservation_id"],
        "reservation_digest": reservation["reservation_digest"],
        "handoff_id": handoff["handoff_id"],
        "handoff_digest": handoff["content_digest"],
        "target_id": handoff["target_id"],
        "run_id": handoff["run_id"],
        "cycle_id": handoff["cycle_id"],
        "branch_id": handoff["branch_id"],
        "action_id": prelaunch["action_id"],
        "action_digest": prelaunch["action_digest"],
        "attempt_id": prelaunch["attempt_id"],
        "attempt_number": prelaunch["attempt_number"],
        "obligation_id": handoff["obligation_id"],
        "formal_claim_digest": handoff["formal_claim_digest"],
        "proof_adapter": handoff["proof_adapter"],
        "execution_plan_digest": handoff["execution_plan_digest"],
        "proof_runtime_ref": runtime_ref,
        "runtime_contract_digest": canonical_digest(runtime_contract),
        "resource_budget_digest": resource_budget_digest,
        "execution_policy_digest": canonical_digest(execution_policy),
        "source_theory_head_digest": prelaunch["source_theory_head_digest"],
        "claim_reference_record_digest": bytes_digest(
            binding._execution_claim_bytes
        ),
        "claim_reference_record_bytes": len(binding._execution_claim_bytes),
        "executor_lease_id": executor_lease["lease_id"],
        "executor_lease_digest": executor_lease["lease_digest"],
        "executor_lease_expires_at": executor_lease["expires_at"],
        "launch_boundary_checkpoint_required": True,
        "serialized_execution_authority": False,
        "authoritative_for_launch_or_retry": False,
        "launch_performed": False,
        "authority_nulls": dict(PROOF_EXECUTION_AUTHORITY_NULLS),
    }
    projection["binding_id"] = stable_identifier(
        "proof-execution-claim-binding-v1",
        projection["capability_projection_digest"],
        projection["execution_claim_digest"],
        projection["execution_claim_reference_digest"],
        projection["handoff_digest"],
    )
    projection["content_digest"] = _self_digest(projection)
    return projection, budget


def build_proof_execution_claim_binding(
    *,
    prelaunch_projection: Mapping[str, Any],
    handoff: Mapping[str, Any],
    reservation: Mapping[str, Any],
    execution_claim: Mapping[str, Any],
    execution_claim_reference: Mapping[str, Any],
) -> ProofExecutionClaimBinding:
    """Build inert exact evidence from the live capability consumer's result."""

    return ProofExecutionClaimBinding.from_consumed_records(
        prelaunch_projection=prelaunch_projection,
        handoff=handoff,
        reservation=reservation,
        execution_claim=execution_claim,
        execution_claim_reference=execution_claim_reference,
    )


def validate_proof_execution_claim_binding(
    binding: ProofExecutionClaimBinding,
) -> dict[str, Any]:
    """Rebuild a binding from its private bytes and return a defensive copy."""

    if type(binding) is not ProofExecutionClaimBinding:
        raise ProofExecutionContractError(
            "proof execution requires an exact claim-binding object"
        )
    expected, expected_budget = _claim_binding_projection(binding)
    supplied = _decode_mapping(binding._projection_bytes, "proof claim binding")
    if supplied != expected or binding.resource_budget != expected_budget:
        raise ProofExecutionContractError("proof claim binding changed after creation")
    return supplied


def _artifact_policy(
    route: ProofRuntimeRoute, handoff: Mapping[str, Any]
) -> str:
    if route.artifact_policy != "execution_plan_bound":
        return route.artifact_policy
    plan = handoff["execution_plan"]
    supplied = plan.get("artifact_policy")
    if supplied == "none":
        return "forbidden"
    if supplied == "required_new_regular_file":
        return "required_fresh_regular_file"
    raise ProofExecutionContractError(
        "external checker artifact policy is not registered"
    )


def build_exact_lean_source(
    binding: ProofExecutionClaimBinding,
) -> StagedByteArtifact:
    """Derive the only accepted Lean source bytes from the bound formal claim."""

    validate_proof_execution_claim_binding(binding)
    handoff = binding.handoff
    if handoff["proof_adapter"] != "lean":
        raise ProofExecutionContractError(
            "Lean source can be derived only for the Lean route"
        )
    claim = handoff["formal_claim"]
    if claim.get("claim_kind") != "lean_proposition":
        raise ProofExecutionContractError("Lean route has a non-Lean formal claim")
    imports = claim.get("imports")
    proposition = claim.get("proposition")
    proof_term = claim.get("proof_term")
    axiom_policy = claim.get("axiom_policy")
    if (
        not isinstance(imports, list)
        or imports != list(dict.fromkeys(imports))
        or any(
            not isinstance(name, str)
            or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.]*", name)
            for name in imports
        )
        or not isinstance(proposition, str)
        or not proposition.strip()
        or not isinstance(proof_term, str)
        or not proof_term.strip()
        or axiom_policy != "no_nonstandard_axioms"
    ):
        raise ProofExecutionContractError("Lean claim source fields are invalid")
    forbidden = re.compile(r"(?i)(?:\bsorry\b|\badmit\b|\baxiom\b)")
    if forbidden.search(proof_term):
        raise ProofExecutionContractError(
            "Lean proof term contains an admission or caller-authored axiom"
        )
    source = "".join(f"import {name}\n" for name in imports)
    source += (
        f"theorem abducer_claim : {proposition} := {proof_term}\n"
        "#print axioms abducer_claim\n"
    )
    return StagedByteArtifact.from_bytes(
        "workspace/Claim.lean",
        source.encode("utf-8"),
        roles=("source",),
    )


def _proof_worker_request(
    binding: ProofExecutionClaimBinding,
    route: ProofRuntimeRoute,
    artifact_policy: str,
) -> dict[str, Any]:
    projection = validate_proof_execution_claim_binding(binding)
    handoff = binding.handoff
    request: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": STAGED_INVOCATION_CONTRACT_VERSION,
        "message_kind": "proof_execution_request",
        "binding_id": projection["binding_id"],
        "binding_digest": projection["content_digest"],
        "execution_claim_id": projection["execution_claim_id"],
        "execution_claim_digest": projection["execution_claim_digest"],
        "reservation_id": projection["reservation_id"],
        "reservation_digest": projection["reservation_digest"],
        "attempt_id": projection["attempt_id"],
        "attempt_number": projection["attempt_number"],
        "handoff_id": projection["handoff_id"],
        "handoff_digest": projection["handoff_digest"],
        "formal_claim": handoff["formal_claim"],
        "formal_claim_digest": projection["formal_claim_digest"],
        "adapter": route.adapter,
        "runtime_route_id": route.route_id,
        "runtime_route_digest": route.projection()["content_digest"],
        "execution_plan": handoff["execution_plan"],
        "execution_plan_digest": projection["execution_plan_digest"],
        "artifact_policy": artifact_policy,
        "resource_budget": dataclasses.asdict(binding.resource_budget),
        "resource_budget_digest": projection["resource_budget_digest"],
        "execution_policy": handoff["execution_policy"],
        "execution_policy_digest": projection["execution_policy_digest"],
        "proof_runtime_ref": projection["proof_runtime_ref"],
        "authority_nulls": dict(PROOF_EXECUTION_AUTHORITY_NULLS),
    }
    request["request_id"] = stable_identifier(
        "proof-execution-request-v1",
        projection["binding_id"],
        projection["content_digest"],
        route.route_id,
        projection["attempt_id"],
    )
    request["content_digest"] = _self_digest(request)
    return request


@dataclasses.dataclass(frozen=True, slots=True)
class StagedProofInvocation:
    """A complete immutable byte plan that is explicitly not launch authority."""

    claim_binding: ProofExecutionClaimBinding
    runtime_route: ProofRuntimeRoute
    stdin: StagedByteArtifact
    files: tuple[StagedByteArtifact, ...]
    logical_argv: tuple[str, ...]
    materialized_argv: tuple[str, ...]
    artifact_policy: str
    _dependency_authority_bytes: bytes = dataclasses.field(repr=False)
    _executable_authority_bytes: bytes = dataclasses.field(repr=False)
    _projection_bytes: bytes = dataclasses.field(init=False, repr=False)

    def __post_init__(self) -> None:
        projection = _staged_invocation_projection(self)
        object.__setattr__(self, "_projection_bytes", canonical_json(projection))

    @property
    def dependency_authority(self) -> Mapping[str, Any]:
        return _decode_mapping(
            self._dependency_authority_bytes, "proof dependency authority"
        )

    @property
    def executable_authority(self) -> Mapping[str, Any]:
        return _decode_mapping(
            self._executable_authority_bytes, "proof executable authority"
        )

    @property
    def resource_budget(self) -> ResourceBudget:
        return self.claim_binding.resource_budget

    @property
    def projection(self) -> Mapping[str, Any]:
        return _decode_mapping(self._projection_bytes, "staged proof invocation")


def _staged_invocation_projection(
    invocation: StagedProofInvocation,
) -> dict[str, Any]:
    binding = validate_proof_execution_claim_binding(invocation.claim_binding)
    route = resolve_proof_runtime_route(binding["proof_adapter"])
    if invocation.runtime_route != route:
        raise ProofExecutionContractError(
            "staged invocation route differs from the closed registry"
        )
    dependency_authority = _validate_dependency_authority_projection(
        _decode_mapping(
            invocation._dependency_authority_bytes, "proof dependency authority"
        )
    )
    executable_authority = _validate_executable_authority_projection(
        _decode_mapping(
            invocation._executable_authority_bytes,
            "proof executable authority",
        )
    )
    argv = _validate_argv(invocation.logical_argv)
    if argv != (route.logical_entrypoint,):
        raise ProofExecutionContractError(
            "staged logical argv is not the exact closed-registry token"
        )
    materialized_argv = _validate_argv(invocation.materialized_argv)
    runtime_root = Path(materialized_argv[3]).parents[2]
    runtime_ref_parts = Path(binding["proof_runtime_ref"]).parts
    if (
        route.adapter not in {"exact", "finite_model"}
        or len(materialized_argv) != 4
        or materialized_argv
        != (
            executable_authority["source_path"],
            "-I",
            "-B",
            str(
                runtime_root
                / "agentic/scripts/run_discovery_proof_worker_v3.py"
            ),
        )
        or not runtime_root.is_absolute()
        or tuple(runtime_root.parts[-len(runtime_ref_parts) :])
        != runtime_ref_parts
    ):
        raise ProofExecutionContractError(
            "materialized argv is not the exact runtime-derived built-in command"
        )
    if (
        type(invocation.stdin) is not StagedByteArtifact
        or invocation.stdin.roles != ("stdin",)
        or invocation.stdin.executable
        or invocation.stdin.relative_path != "requests/proof-execution.json"
    ):
        raise ProofExecutionContractError(
            "staged proof stdin is not the exact request attachment"
        )
    expected_request = _proof_worker_request(
        invocation.claim_binding, route, invocation.artifact_policy
    )
    if invocation.stdin.content != canonical_json(expected_request):
        raise ProofExecutionContractError(
            "staged proof stdin differs from the claim-derived request"
        )
    policy_limit = invocation.claim_binding.handoff["execution_policy"][
        "input_limit_bytes"
    ]
    if invocation.stdin.byte_length > policy_limit:
        raise ProofExecutionContractError(
            "staged proof stdin exceeds the bound execution policy"
        )

    if type(invocation.files) is not tuple or len(invocation.files) > MAX_STAGED_FILES:
        raise ProofExecutionContractError("staged proof file cardinality is invalid")
    sorted_files = tuple(
        sorted(invocation.files, key=lambda item: item.relative_path)
    )
    if invocation.files != sorted_files or any(
        type(item) is not StagedByteArtifact for item in invocation.files
    ):
        raise ProofExecutionContractError(
            "staged proof files must be exact objects in canonical path order"
        )
    paths = [invocation.stdin.relative_path, *[item.relative_path for item in invocation.files]]
    if len(paths) != len(set(paths)):
        raise ProofExecutionContractError("staged proof file paths are not unique")
    total_bytes = invocation.stdin.byte_length + sum(
        item.byte_length for item in invocation.files
    )
    if total_bytes > MAX_STAGED_TOTAL_BYTES:
        raise ProofExecutionContractError(
            "staged proof invocation exceeds its total byte ceiling"
        )
    executable_files = [
        item for item in invocation.files if "executable" in item.roles
    ]
    if len(executable_files) != 1:
        raise ProofExecutionContractError(
            "staged proof invocation must contain one exact executable"
        )
    executable = executable_files[0]
    if (
        executable.relative_path
        != executable_authority["staged_relative_path"]
        or executable.content_digest != executable_authority["sha256"]
        or executable.byte_length != executable_authority["byte_length"]
        or "python_runtime" not in executable.roles
    ):
        raise ProofExecutionContractError(
            "staged executable differs from current-process Python authority"
        )
    source_files = [item for item in invocation.files if "source" in item.roles]
    if route.source_policy == "forbidden" and source_files:
        raise ProofExecutionContractError(
            "runtime route forbids staged source files"
        )
    if route.source_policy == "required_exact_lean_source":
        expected_source = build_exact_lean_source(invocation.claim_binding)
        if source_files != [expected_source]:
            raise ProofExecutionContractError(
                "Lean route lacks its one exact derived source file"
            )

    authority_entries = {
        row["path"]: row for row in dependency_authority["entries"]
    }
    dependency_files = {
        item.relative_path: item
        for item in invocation.files
        if "dependency" in item.roles
    }
    if set(dependency_files) != set(authority_entries):
        raise ProofExecutionContractError(
            "staged dependency files differ from the complete authority closure"
        )
    for path, row in authority_entries.items():
        artifact = dependency_files[path]
        if (
            artifact.byte_length != row["byte_size"]
            or artifact.content_digest != row["content_digest"]
            or not set(row["roles"]).issubset(artifact.roles)
        ):
            raise ProofExecutionContractError(
                f"staged dependency bytes differ from authority: {path}"
            )

    expected_artifact_policy = _artifact_policy(
        route, invocation.claim_binding.handoff
    )
    if invocation.artifact_policy != expected_artifact_policy:
        raise ProofExecutionContractError(
            "staged result-artifact policy differs from the closed route"
        )
    route_projection = route.projection()
    file_descriptors = [item.descriptor() for item in invocation.files]
    projection: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": STAGED_INVOCATION_CONTRACT_VERSION,
        "invocation_kind": "immutable_claim_bound_proof_execution_stage",
        "binding_id": binding["binding_id"],
        "binding_digest": binding["content_digest"],
        "execution_claim_id": binding["execution_claim_id"],
        "execution_claim_digest": binding["execution_claim_digest"],
        "reservation_id": binding["reservation_id"],
        "reservation_digest": binding["reservation_digest"],
        "attempt_id": binding["attempt_id"],
        "attempt_number": binding["attempt_number"],
        "handoff_id": binding["handoff_id"],
        "handoff_digest": binding["handoff_digest"],
        "target_id": binding["target_id"],
        "run_id": binding["run_id"],
        "cycle_id": binding["cycle_id"],
        "branch_id": binding["branch_id"],
        "obligation_id": binding["obligation_id"],
        "formal_claim_digest": binding["formal_claim_digest"],
        "proof_adapter": binding["proof_adapter"],
        "runtime_route": route_projection,
        "logical_argv": list(argv),
        "materialized_argv": list(materialized_argv),
        "proof_runtime_ref": binding["proof_runtime_ref"],
        "stdin": invocation.stdin.descriptor(),
        "files": file_descriptors,
        "dependency_authority_digest": dependency_authority["content_digest"],
        "executable_authority": executable_authority,
        "resource_budget": dataclasses.asdict(invocation.resource_budget),
        "resource_budget_digest": binding["resource_budget_digest"],
        "execution_policy": invocation.claim_binding.handoff["execution_policy"],
        "execution_policy_digest": binding["execution_policy_digest"],
        "artifact_policy": invocation.artifact_policy,
        "total_staged_bytes": total_bytes,
        "launch_implemented": True,
        "launch_performed": False,
        "projection_only": True,
        "authoritative_for_launch_or_retry": False,
        "authority_nulls": dict(PROOF_EXECUTION_AUTHORITY_NULLS),
    }
    projection["invocation_id"] = stable_identifier(
        "staged-proof-invocation-v1",
        projection["binding_digest"],
        projection["runtime_route"]["content_digest"],
        projection["stdin"],
        projection["files"],
        projection["dependency_authority_digest"],
    )
    projection["content_digest"] = _self_digest(projection)
    return projection


def build_staged_proof_invocation(
    binding: ProofExecutionClaimBinding,
    *,
    dependency_profile: ProofDependencyProfile,
    dependency_authority: Mapping[str, Any],
    files: Sequence[StagedByteArtifact],
    materialized_runtime_root: Path | str,
    executable_authority: Mapping[str, Any],
    repository_root: Path | str = ROOT,
) -> StagedProofInvocation:
    """Build a launch-free staged invocation from exact post-CAS evidence.

    ``files`` must already contain the complete dependency closure, at least
    one exact executable attachment, and the derived Lean source when the
    selected route is Lean.  The logical argv and canonical stdin are never
    caller-selected.
    """

    binding_projection = validate_proof_execution_claim_binding(binding)
    expected_authority = dependency_profile.validate_authority(
        dependency_authority, repository_root=repository_root
    )
    route = resolve_proof_runtime_route(binding_projection["proof_adapter"])
    if route.adapter not in {"exact", "finite_model"}:
        raise ProofExecutionContractError(
            "unavailable proof route cannot produce a staged invocation"
        )
    artifact_policy = _artifact_policy(route, binding.handoff)
    request = _proof_worker_request(binding, route, artifact_policy)
    stdin = StagedByteArtifact.from_bytes(
        "requests/proof-execution.json",
        canonical_json(request),
        roles=("stdin",),
    )
    canonical_files = tuple(sorted(tuple(files), key=lambda item: item.relative_path))
    runtime_root = Path(materialized_runtime_root)
    if not runtime_root.is_absolute():
        raise ProofExecutionContractError(
            "materialized proof runtime root must be absolute"
        )
    return StagedProofInvocation(
        claim_binding=binding,
        runtime_route=route,
        stdin=stdin,
        files=canonical_files,
        logical_argv=(route.logical_entrypoint,),
        materialized_argv=(
            str(executable_authority["source_path"]),
            "-I",
            "-B",
            str(
                runtime_root
                / "agentic/scripts/run_discovery_proof_worker_v3.py"
            ),
        ),
        artifact_policy=artifact_policy,
        _dependency_authority_bytes=canonical_json(expected_authority),
        _executable_authority_bytes=canonical_json(
            _validate_executable_authority_projection(executable_authority)
        ),
    )


def validate_staged_proof_invocation(
    invocation: StagedProofInvocation,
) -> dict[str, Any]:
    """Rebuild every descriptor and reject post-construction substitution."""

    if type(invocation) is not StagedProofInvocation:
        raise ProofExecutionContractError(
            "proof execution requires an exact staged invocation"
        )
    expected = _staged_invocation_projection(invocation)
    supplied = _decode_mapping(
        invocation._projection_bytes, "staged proof invocation"
    )
    if supplied != expected:
        raise ProofExecutionContractError(
            "staged proof invocation changed after construction"
        )
    return supplied


_STAGED_PROJECTION_KEYS = frozenset(
    {
        "schema_version",
        "contract_version",
        "invocation_kind",
        "binding_id",
        "binding_digest",
        "execution_claim_id",
        "execution_claim_digest",
        "reservation_id",
        "reservation_digest",
        "attempt_id",
        "attempt_number",
        "handoff_id",
        "handoff_digest",
        "target_id",
        "run_id",
        "cycle_id",
        "branch_id",
        "obligation_id",
        "formal_claim_digest",
        "proof_adapter",
        "runtime_route",
        "logical_argv",
        "materialized_argv",
        "proof_runtime_ref",
        "stdin",
        "files",
        "dependency_authority_digest",
        "executable_authority",
        "resource_budget",
        "resource_budget_digest",
        "execution_policy",
        "execution_policy_digest",
        "artifact_policy",
        "total_staged_bytes",
        "launch_implemented",
        "launch_performed",
        "projection_only",
        "authoritative_for_launch_or_retry",
        "authority_nulls",
        "invocation_id",
        "content_digest",
    }
)


def validate_staged_invocation_projection(
    projection: Mapping[str, Any],
    *,
    expected_binding_digest: str | None = None,
) -> dict[str, Any]:
    """Decode inert historical evidence without granting current authority."""

    payload = _decode_mapping(
        _canonical_mapping_bytes(projection, "staged invocation projection"),
        "staged invocation projection",
    )
    _require_exact_keys(payload, _STAGED_PROJECTION_KEYS, "staged invocation")
    _require_self_digest(payload, label="staged invocation")
    if (
        payload["schema_version"] != 1
        or payload["contract_version"] != STAGED_INVOCATION_CONTRACT_VERSION
        or payload["invocation_kind"]
        != "immutable_claim_bound_proof_execution_stage"
        or payload["launch_implemented"] is not True
        or payload["launch_performed"] is not False
        or payload["projection_only"] is not True
        or payload["authoritative_for_launch_or_retry"] is not False
    ):
        raise ProofExecutionContractError(
            "staged invocation projection overstates execution authority"
        )
    _validate_authority_nulls(
        payload["authority_nulls"], "staged invocation projection"
    )
    if (
        expected_binding_digest is not None
        and payload["binding_digest"] != expected_binding_digest
    ):
        raise ProofExecutionContractError(
            "staged invocation projection crossed its claim binding"
        )
    return payload


def build_resource_governor_for_staged_invocation(
    invocation: StagedProofInvocation,
    *,
    execution_root: Path | str,
) -> ResourceGovernor:
    """Construct, but never run, the shared ResourceGovernor.

    The runtime directory is derived from the claim-bound relative reference;
    callers cannot provide an attempt subdirectory or alternate command.  This
    helper intentionally does not create directories or call ``run_process``.
    """

    projection = validate_staged_proof_invocation(invocation)
    root = Path(execution_root)
    if root.is_symlink() or not root.is_dir():
        raise ProofExecutionContractError(
            "proof execution root must be an existing non-symlink directory"
        )
    root = root.resolve(strict=True)
    try:
        runtime_root = safe_relative_path(
            projection["proof_runtime_ref"], root, forbid_latest=True
        )
    except ContractError as exc:
        raise ProofExecutionContractError(
            "proof runtime root cannot be derived inside the execution root"
        ) from exc
    policy = projection["execution_policy"]
    capture_limit = max(
        policy["stdout_limit_bytes"], policy["stderr_limit_bytes"]
    )
    return ResourceGovernor(
        invocation.resource_budget,
        run_directory=runtime_root,
        allowed_working_directory=runtime_root,
        capture_limit_bytes=capture_limit,
    )


@dataclasses.dataclass(frozen=True, slots=True)
class _TerminalShape:
    phase: str
    launch_disposition: str
    allowed_execution_statuses: frozenset[str]
    invocation_required: bool
    process_required: bool
    checker_output_required: bool


_RESOURCE_FAILURES = frozenset(GOVERNOR_TERMINAL_STATUSES - {"succeeded"})
_TERMINAL_SHAPES: Mapping[str, _TerminalShape] = MappingProxyType(
    {
        "staging_rejected": _TerminalShape(
            "staging", "not_attempted", frozenset({"not_started"}), False, False, False
        ),
        "governor_rejected": _TerminalShape(
            "governor_setup",
            "not_attempted",
            frozenset({"not_started"}),
            True,
            False,
            False,
        ),
        "spawn_failed": _TerminalShape(
            "spawn", "not_started", frozenset({"not_started"}), True, False, False
        ),
        "governed_not_started": _TerminalShape(
            "supervision", "not_started", _RESOURCE_FAILURES, True, True, False
        ),
        "process_failed": _TerminalShape(
            "supervision", "started", _RESOURCE_FAILURES, True, True, False
        ),
        "protocol_rejected": _TerminalShape(
            "protocol", "started", frozenset({"succeeded"}), True, True, True
        ),
        "artifact_rejected": _TerminalShape(
            "artifact", "started", frozenset({"succeeded"}), True, True, True
        ),
        "completed": _TerminalShape(
            "complete", "started", frozenset({"succeeded"}), True, True, True
        ),
        "abandoned_uncertain": _TerminalShape(
            "recovery",
            "unknown_after_claim",
            frozenset({"uncertain"}),
            False,
            False,
            False,
        ),
    }
)


@dataclasses.dataclass(frozen=True, slots=True)
class ProofExecutionTerminalResult:
    """One total operational outcome, still outside atomic finalization."""

    claim_binding: ProofExecutionClaimBinding
    invocation: StagedProofInvocation | None
    terminal_status: str
    execution_status: str
    proof_verdict: str
    reason_code: str
    started_at: str
    completed_at: str
    _process_event_bytes: bytes | None = dataclasses.field(default=None, repr=False)
    _resource_receipt_bytes: bytes | None = dataclasses.field(
        default=None, repr=False
    )
    checker_output: bytes | None = dataclasses.field(default=None, repr=False)
    _certificate_bytes: bytes | None = dataclasses.field(default=None, repr=False)
    artifacts: tuple[StagedByteArtifact, ...] = ()
    _projection_bytes: bytes = dataclasses.field(init=False, repr=False)
    _durable_bundle_bytes: bytes | None = dataclasses.field(
        init=False, default=None, repr=False, compare=False
    )
    _durable_commit_reference_bytes: bytes | None = dataclasses.field(
        init=False, default=None, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        projection = _terminal_result_projection(self)
        object.__setattr__(self, "_projection_bytes", canonical_json(projection))

    @property
    def process_event(self) -> Mapping[str, Any] | None:
        if self._process_event_bytes is None:
            return None
        return _decode_mapping(self._process_event_bytes, "proof process event")

    @property
    def resource_receipt(self) -> Mapping[str, Any] | None:
        if self._resource_receipt_bytes is None:
            return None
        return _decode_mapping(
            self._resource_receipt_bytes, "proof resource receipt"
        )

    @property
    def certificate(self) -> Mapping[str, Any] | None:
        if self._certificate_bytes is None:
            return None
        return _decode_mapping(self._certificate_bytes, "proof certificate")

    @property
    def projection(self) -> Mapping[str, Any]:
        return _decode_mapping(self._projection_bytes, "proof terminal result")

    @property
    def durably_finalized(self) -> bool:
        return (
            self._durable_bundle_bytes is not None
            and self._durable_commit_reference_bytes is not None
        )

    @property
    def durable_bundle(self) -> Mapping[str, Any] | None:
        if self._durable_bundle_bytes is None:
            return None
        return _decode_mapping(
            self._durable_bundle_bytes, "durable proof terminal bundle"
        )

    @property
    def durable_commit_reference(self) -> Mapping[str, Any] | None:
        if self._durable_commit_reference_bytes is None:
            return None
        return _decode_mapping(
            self._durable_commit_reference_bytes,
            "durable proof terminal commit reference",
        )


def _checker_response(
    terminal: ProofExecutionTerminalResult,
    process_event: Mapping[str, Any],
    binding: Mapping[str, Any],
) -> dict[str, Any]:
    if type(terminal.checker_output) is not bytes:
        raise ProofExecutionContractError(
            "checker output must be retained as exact bytes"
        )
    if len(terminal.checker_output) > MAX_CHECKER_OUTPUT_BYTES:
        raise ProofExecutionContractError(
            "checker output exceeds the terminal byte ceiling"
        )
    if (
        bytes_digest(terminal.checker_output) != process_event.get("stdout_sha256")
        or len(terminal.checker_output) != process_event.get("stdout_bytes")
        or process_event.get("stdout_truncated") is not False
        or process_event.get("stdout_drain_incomplete") is not False
        or process_event.get("stdout_utf8_valid") is not True
    ):
        raise ProofExecutionContractError(
            "checker output lacks complete exact UTF-8 supervision evidence"
        )
    stripped = terminal.checker_output
    try:
        response = json.loads(stripped.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ProofExecutionContractError(
            "checker output is not one JSON object"
        ) from exc
    if (
        not isinstance(response, dict)
        or canonical_json(response) != stripped
    ):
        raise ProofExecutionContractError(
            "checker output is not one canonical object"
        )
    _require_exact_keys(
        response,
        frozenset(
            {
                "schema_version",
                "contract_version",
                "message_kind",
                "response_id",
                "request_id",
                "binding_id",
                "binding_digest",
                "execution_claim_id",
                "execution_claim_digest",
                "attempt_id",
                "attempt_number",
                "handoff_id",
                "handoff_digest",
                "formal_claim_digest",
                "adapter",
                "runtime_route_id",
                "proof_verdict",
                "result",
                "scoped_certificate",
                "completeness",
                "uncertainty",
                "artifact",
                "authority_boundary",
                "authority_nulls",
                "content_digest",
            }
        ),
        "proof worker response",
    )
    _require_self_digest(response, label="proof worker response")
    if terminal.invocation is None:
        raise ProofExecutionContractError(
            "checker response lacks its staged invocation"
        )
    invocation = validate_staged_proof_invocation(terminal.invocation)
    request = _decode_mapping(
        terminal.invocation.stdin.content, "proof execution request"
    )
    required_matches = {
        "request_id": request["request_id"],
        "binding_id": binding["binding_id"],
        "binding_digest": binding["content_digest"],
        "execution_claim_id": binding["execution_claim_id"],
        "execution_claim_digest": binding["execution_claim_digest"],
        "attempt_id": binding["attempt_id"],
        "attempt_number": binding["attempt_number"],
        "handoff_id": binding["handoff_id"],
        "handoff_digest": binding["handoff_digest"],
        "formal_claim_digest": binding["formal_claim_digest"],
        "adapter": terminal.invocation.runtime_route.adapter,
        "runtime_route_id": terminal.invocation.runtime_route.route_id,
    }
    for field, expected in required_matches.items():
        if response.get(field) != expected:
            raise ProofExecutionContractError(
                f"checker response crossed {field}"
            )
    if (
        response["schema_version"] != 3
        or response["contract_version"] != _WORKER_RESPONSE_CONTRACT_VERSION
        or response["message_kind"] != "proof_execution_response"
        or response["artifact"] is not None
        or response["authority_nulls"] != dict(PROOF_EXECUTION_AUTHORITY_NULLS)
        or not isinstance(response["authority_boundary"], str)
        or len(response["authority_boundary"]) < 32
        or not isinstance(response["result"], Mapping)
        or not isinstance(response["completeness"], Mapping)
        or not isinstance(response["uncertainty"], Mapping)
    ):
        raise ProofExecutionContractError(
            "checker response constants or evidence shape are invalid"
        )
    checker_verdict = response.get("proof_verdict")
    if checker_verdict not in _CHECKER_TO_TERMINAL_VERDICT:
        raise ProofExecutionContractError(
            "checker response verdict is not registered"
        )
    certificate = response["scoped_certificate"]
    decisive = checker_verdict != "inconclusive"
    if decisive:
        if not isinstance(certificate, Mapping):
            raise ProofExecutionContractError(
                "decisive checker response lacks a scoped certificate"
            )
        certificate = dict(certificate)
        _require_self_digest(certificate, label="scoped proof certificate")
        certificate_matches = {
            "request_id": request["request_id"],
            "binding_id": binding["binding_id"],
            "binding_digest": binding["content_digest"],
            "execution_claim_id": binding["execution_claim_id"],
            "execution_claim_digest": binding["execution_claim_digest"],
            "attempt_id": binding["attempt_id"],
            "handoff_id": binding["handoff_id"],
            "handoff_digest": binding["handoff_digest"],
            "formal_claim_digest": binding["formal_claim_digest"],
            "adapter": terminal.invocation.runtime_route.adapter,
        }
        if (
            any(
                certificate.get(field) != expected
                for field, expected in certificate_matches.items()
            )
            or certificate.get("authority_nulls")
            != dict(PROOF_EXECUTION_AUTHORITY_NULLS)
            or type(certificate.get("claim_holds")) is not bool
            or certificate["claim_holds"]
            is not (
                checker_verdict
                == "claim_validated_within_declared_scope"
            )
            or response["result"].get("claim_holds")
            is not certificate["claim_holds"]
            or response["completeness"].get("complete") is not True
        ):
            raise ProofExecutionContractError(
                "scoped proof certificate crossed its response or claim"
            )
    elif certificate is not None:
        raise ProofExecutionContractError(
            "inconclusive checker response must not carry a certificate"
        )
    expected_response_id = stable_identifier(
        "proof-execution-worker-response-v3",
        request["request_id"],
        binding["content_digest"],
        checker_verdict,
        response["result"],
        response["scoped_certificate"],
        response["completeness"],
    )
    if response["response_id"] != expected_response_id:
        raise ProofExecutionContractError(
            "checker response identity is not exactly derived"
        )
    if invocation["runtime_route"]["content_digest"] != request[
        "runtime_route_digest"
    ]:
        raise ProofExecutionContractError(
            "checker response request crossed its runtime route"
        )
    return response


def _validate_process_and_resource(
    terminal: ProofExecutionTerminalResult,
    *,
    invocation_projection: Mapping[str, Any],
    shape: _TerminalShape,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if terminal._process_event_bytes is None or terminal._resource_receipt_bytes is None:
        raise ProofExecutionContractError(
            "terminal outcome lacks process or resource evidence"
        )
    process = _decode_mapping(
        terminal._process_event_bytes, "proof process event"
    )
    resource = _decode_mapping(
        terminal._resource_receipt_bytes, "proof resource receipt"
    )
    if (
        process.get("event") != "process_terminal"
        or process.get("role") != "solver"
        or process.get("command") != invocation_projection["materialized_argv"]
        or process.get("status") != terminal.execution_status
        or process.get("stdin_sha256")
        != invocation_projection["stdin"]["sha256"]
        or process.get("stdin_bytes")
        != invocation_projection["stdin"]["byte_length"]
    ):
        raise ProofExecutionContractError(
            "process event differs from the staged invocation"
        )
    pid = process.get("pid")
    if shape.launch_disposition == "started" and (
        isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0
    ):
        raise ProofExecutionContractError(
            "started proof process lacks a positive PID"
        )
    if shape.launch_disposition == "not_started" and pid is not None:
        raise ProofExecutionContractError(
            "not-started proof process unexpectedly has a PID"
        )
    if process.get("epistemic_effect") not in {
        "none_operational_outcome_only",
        "awaiting_output_validation",
    }:
        raise ProofExecutionContractError(
            "process event overstates its epistemic effect"
        )
    events = resource.get("events")
    if (
        resource.get("budget") != invocation_projection["resource_budget"]
        or not isinstance(events, list)
        or events != [process]
    ):
        raise ProofExecutionContractError(
            "resource receipt does not replay one exact governed process"
        )
    runtime_root = Path(invocation_projection["materialized_argv"][3]).parents[2]
    try:
        expected_environment = complete_governed_process_environment(
            minimal_replacement_environment(
                runtime_root, create_temporary=False
            ),
            deadline=resource["deadline"],
            budget=resource["budget"],
        )
        attempt = validate_v2_process_event(
            process,
            accepted=process["status"] == "succeeded",
            expected_workspace=runtime_root,
            expected_replacement_environment=expected_environment,
            require_live_execution_authority=True,
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ProofExecutionContractError(
            f"proof process v2 authority replay failed: {exc}"
        ) from exc
    if shape.launch_disposition == "started" and attempt is None:
        raise ProofExecutionContractError(
            "started proof process lacks supervised attempt evidence"
        )
    return process, resource


def _terminal_artifact_policy(
    invocation: StagedProofInvocation,
    artifacts: tuple[StagedByteArtifact, ...],
) -> None:
    policy = invocation.artifact_policy
    if policy == "forbidden" and artifacts:
        raise ProofExecutionContractError(
            "terminal result contains a forbidden checker artifact"
        )
    if policy == "required_fresh_regular_file" and len(artifacts) != 1:
        raise ProofExecutionContractError(
            "terminal result lacks one required checker artifact"
        )
    for artifact in artifacts:
        if "result_artifact" not in artifact.roles or artifact.executable:
            raise ProofExecutionContractError(
                "terminal artifact has the wrong immutable role"
            )


def _terminal_result_projection(
    terminal: ProofExecutionTerminalResult,
) -> dict[str, Any]:
    binding = validate_proof_execution_claim_binding(terminal.claim_binding)
    try:
        shape = _TERMINAL_SHAPES[terminal.terminal_status]
    except (KeyError, TypeError) as exc:
        raise ProofExecutionContractError(
            f"proof terminal status is unregistered: {terminal.terminal_status!r}"
        ) from exc
    if terminal.execution_status not in shape.allowed_execution_statuses:
        raise ProofExecutionContractError(
            "proof terminal and execution statuses are inconsistent"
        )
    if terminal.proof_verdict not in TERMINAL_PROOF_VERDICTS:
        raise ProofExecutionContractError("proof terminal verdict is unregistered")
    if terminal.terminal_status != "completed":
        if terminal.proof_verdict != "not_evaluated":
            raise ProofExecutionContractError(
                "non-completed execution cannot carry a proof verdict"
            )
    elif terminal.proof_verdict == "not_evaluated":
        raise ProofExecutionContractError(
            "completed execution must carry an explicitly scoped verdict"
        )
    reason_code = _validated_reason_code(terminal.reason_code)
    started = _validated_utc_seconds(terminal.started_at, "terminal started_at")
    completed = _validated_utc_seconds(
        terminal.completed_at, "terminal completed_at"
    )
    if completed < started:
        raise ProofExecutionContractError(
            "proof terminal completed_at precedes started_at"
        )

    invocation_projection: dict[str, Any] | None = None
    if terminal.invocation is not None:
        invocation_projection = validate_staged_proof_invocation(
            terminal.invocation
        )
        if terminal.invocation.claim_binding != terminal.claim_binding:
            raise ProofExecutionContractError(
                "terminal invocation crossed its proof claim binding"
            )
    invocation_required = shape.invocation_required
    if terminal.terminal_status == "abandoned_uncertain":
        if reason_code == "launch_not_observed_abandoned":
            invocation_required = False
        elif reason_code == "execution_outcome_unknown_abandoned":
            invocation_required = True
        else:
            raise ProofExecutionContractError(
                "abandoned proof terminal reason is unregistered"
            )
    if invocation_required != (invocation_projection is not None):
        raise ProofExecutionContractError(
            "terminal invocation presence differs from its phase contract"
        )

    process: dict[str, Any] | None = None
    resource: dict[str, Any] | None = None
    if shape.process_required:
        assert invocation_projection is not None
        process, resource = _validate_process_and_resource(
            terminal,
            invocation_projection=invocation_projection,
            shape=shape,
        )
    elif (
        terminal._process_event_bytes is not None
        or terminal._resource_receipt_bytes is not None
    ):
        raise ProofExecutionContractError(
            "terminal phase forbids process and resource evidence"
        )

    response: dict[str, Any] | None = None
    if shape.checker_output_required:
        assert process is not None
        if type(terminal.checker_output) is not bytes:
            raise ProofExecutionContractError(
                "terminal phase requires an exact checker-output attachment"
            )
        try:
            response = _checker_response(terminal, process, binding)
        except ProofExecutionContractError:
            if terminal.terminal_status != "protocol_rejected":
                raise
            response = None
    elif terminal.checker_output is not None:
        raise ProofExecutionContractError(
            "terminal phase forbids checker output"
        )
    if terminal.terminal_status == "protocol_rejected" and response is not None:
        raise ProofExecutionContractError(
            "protocol_rejected terminal contains an accepted response"
        )
    if terminal.terminal_status in {"artifact_rejected", "completed"} and response is None:
        raise ProofExecutionContractError(
            "terminal phase requires an accepted checker response"
        )
    if response is not None:
        expected_verdict = _CHECKER_TO_TERMINAL_VERDICT[response["proof_verdict"]]
        if terminal.terminal_status == "completed":
            if terminal.proof_verdict != expected_verdict:
                raise ProofExecutionContractError(
                    "terminal verdict differs from the checker response"
                )
        elif terminal.proof_verdict != "not_evaluated":
            raise ProofExecutionContractError(
                "rejected checker material cannot carry a proof verdict"
            )

    certificate: dict[str, Any] | None = None
    if terminal._certificate_bytes is not None:
        certificate = _decode_mapping(
            terminal._certificate_bytes, "proof certificate"
        )
        _require_self_digest(certificate, label="proof certificate")
        if (
            certificate.get("formal_claim_digest")
            != binding["formal_claim_digest"]
            or certificate.get("handoff_digest") != binding["handoff_digest"]
        ):
            raise ProofExecutionContractError(
                "proof certificate crossed its exact claim or handoff"
            )
    expected_certificate = (
        None if response is None else response.get("scoped_certificate")
    )
    if certificate != expected_certificate:
        raise ProofExecutionContractError(
            "terminal certificate differs from the accepted checker response"
        )
    decisive = terminal.proof_verdict not in {"not_evaluated", "inconclusive"}
    if decisive != (certificate is not None):
        raise ProofExecutionContractError(
            "decisive checker report and scoped certificate presence differ"
        )
    if terminal.terminal_status != "completed" and certificate is not None:
        raise ProofExecutionContractError(
            "rejected execution cannot retain an accepted certificate"
        )

    if type(terminal.artifacts) is not tuple or tuple(
        sorted(terminal.artifacts, key=lambda item: item.relative_path)
    ) != terminal.artifacts:
        raise ProofExecutionContractError(
            "terminal artifacts must be a canonical tuple"
        )
    if terminal.terminal_status == "completed":
        assert terminal.invocation is not None
        _terminal_artifact_policy(terminal.invocation, terminal.artifacts)
    elif terminal.artifacts:
        raise ProofExecutionContractError(
            "non-completed terminal cannot retain accepted result artifacts"
        )

    checker_descriptor = (
        None
        if terminal.checker_output is None
        else {
            "sha256": bytes_digest(terminal.checker_output),
            "byte_length": len(terminal.checker_output),
            "canonical_response_accepted": response is not None,
        }
    )
    projection: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": TERMINAL_RESULT_CONTRACT_VERSION,
        "terminal_kind": "total_proof_execution_operational_result",
        "binding_id": binding["binding_id"],
        "binding_digest": binding["content_digest"],
        "execution_claim_id": binding["execution_claim_id"],
        "execution_claim_digest": binding["execution_claim_digest"],
        "reservation_id": binding["reservation_id"],
        "reservation_digest": binding["reservation_digest"],
        "attempt_id": binding["attempt_id"],
        "attempt_number": binding["attempt_number"],
        "handoff_id": binding["handoff_id"],
        "handoff_digest": binding["handoff_digest"],
        "formal_claim_digest": binding["formal_claim_digest"],
        "invocation_id": (
            None if invocation_projection is None else invocation_projection["invocation_id"]
        ),
        "invocation_digest": (
            None
            if invocation_projection is None
            else invocation_projection["content_digest"]
        ),
        "terminal_status": terminal.terminal_status,
        "terminal_phase": shape.phase,
        "launch_disposition": shape.launch_disposition,
        "execution_status": terminal.execution_status,
        "proof_verdict": terminal.proof_verdict,
        "reason_code": reason_code,
        "started_at": terminal.started_at,
        "completed_at": terminal.completed_at,
        "process_event": process,
        "process_event_digest": (
            None if process is None else canonical_digest(process)
        ),
        "resource_receipt": resource,
        "resource_receipt_digest": (
            None if resource is None else canonical_digest(resource)
        ),
        "checker_output": checker_descriptor,
        "certificate": certificate,
        "certificate_digest": (
            None if certificate is None else canonical_digest(certificate)
        ),
        "artifacts": [artifact.descriptor() for artifact in terminal.artifacts],
        "epistemic_effect": "none_operational_result_pending_distinct_n_plus_one_intake",
        "persisted": False,
        "authoritative_for_atomic_finalization": False,
        "pending_n_plus_one_reflection_created": False,
        "same_cycle_theory_mutation": False,
        "authority_nulls": dict(PROOF_EXECUTION_AUTHORITY_NULLS),
    }
    projection["terminal_id"] = stable_identifier(
        "proof-execution-terminal-v1",
        projection["binding_digest"],
        projection["invocation_digest"],
        projection["terminal_status"],
        projection["execution_status"],
        projection["proof_verdict"],
        projection["reason_code"],
        projection["process_event_digest"],
        projection["resource_receipt_digest"],
        projection["checker_output"],
        projection["certificate_digest"],
        projection["artifacts"],
        projection["started_at"],
        projection["completed_at"],
    )
    projection["content_digest"] = _self_digest(projection)
    return projection


def build_proof_execution_terminal_result(
    binding: ProofExecutionClaimBinding,
    *,
    terminal_status: str,
    execution_status: str,
    proof_verdict: str,
    reason_code: str,
    started_at: str,
    completed_at: str,
    invocation: StagedProofInvocation | None = None,
    process_event: Mapping[str, Any] | None = None,
    resource_receipt: Mapping[str, Any] | None = None,
    checker_output: bytes | None = None,
    certificate: Mapping[str, Any] | None = None,
    artifacts: Sequence[StagedByteArtifact] = (),
) -> ProofExecutionTerminalResult:
    """Build one deterministic total result from already observed evidence."""

    validate_proof_execution_claim_binding(binding)
    if checker_output is not None and type(checker_output) is not bytes:
        raise ProofExecutionContractError("checker_output must be exact bytes")
    canonical_artifacts = tuple(
        sorted(tuple(artifacts), key=lambda item: item.relative_path)
    )
    return ProofExecutionTerminalResult(
        claim_binding=binding,
        invocation=invocation,
        terminal_status=terminal_status,
        execution_status=execution_status,
        proof_verdict=proof_verdict,
        reason_code=reason_code,
        started_at=started_at,
        completed_at=completed_at,
        _process_event_bytes=(
            None
            if process_event is None
            else _canonical_mapping_bytes(process_event, "proof process event")
        ),
        _resource_receipt_bytes=(
            None
            if resource_receipt is None
            else _canonical_mapping_bytes(
                resource_receipt, "proof resource receipt"
            )
        ),
        checker_output=(
            None
            if checker_output is None
            else memoryview(checker_output).tobytes()
        ),
        _certificate_bytes=(
            None
            if certificate is None
            else _canonical_mapping_bytes(certificate, "proof certificate")
        ),
        artifacts=canonical_artifacts,
    )


def build_staging_rejection_terminal(
    binding: ProofExecutionClaimBinding,
    *,
    reason_code: str,
    observed_at: str,
) -> ProofExecutionTerminalResult:
    """Totalize a post-claim staging failure without inventing process evidence."""

    return build_proof_execution_terminal_result(
        binding,
        terminal_status="staging_rejected",
        execution_status="not_started",
        proof_verdict="not_evaluated",
        reason_code=reason_code,
        started_at=observed_at,
        completed_at=observed_at,
    )


def validate_proof_execution_terminal_result(
    terminal: ProofExecutionTerminalResult,
) -> dict[str, Any]:
    """Rebuild a terminal result and reject any post-construction substitution."""

    if type(terminal) is not ProofExecutionTerminalResult:
        raise ProofExecutionContractError(
            "proof terminal validation requires an exact result object"
        )
    expected = _terminal_result_projection(terminal)
    supplied = _decode_mapping(terminal._projection_bytes, "proof terminal result")
    if supplied != expected:
        raise ProofExecutionContractError(
            "proof terminal result changed after construction"
        )
    return supplied


_REPLAY_BINDING_COMPONENTS = MappingProxyType(
    {
        "typed_replay/binding/prelaunch-projection.json": (
            "_prelaunch_projection_bytes"
        ),
        "typed_replay/binding/handoff.json": "_handoff_bytes",
        "typed_replay/binding/reservation.json": "_reservation_bytes",
        "typed_replay/binding/execution-claim.json": (
            "_execution_claim_bytes"
        ),
        "typed_replay/binding/execution-claim-reference.json": (
            "_execution_claim_reference_bytes"
        ),
    }
)
_REPLAY_BINDING_PROJECTION = "typed_replay/binding/projection.json"
_REPLAY_INVOCATION_PROJECTION = "typed_replay/invocation/projection.json"
_REPLAY_INVOCATION_DEPENDENCY_AUTHORITY = (
    "typed_replay/invocation/dependency-authority.json"
)
_REPLAY_INVOCATION_EXECUTABLE_AUTHORITY = (
    "typed_replay/invocation/executable-authority.json"
)
_REPLAY_INVOCATION_STDIN = "typed_replay/invocation/stdin.bin"
_REPLAY_INVOCATION_FILE_PREFIX = "typed_replay/invocation/files/"
TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT = (
    "typed_replay/checkpoint/launch-boundary.json"
)
_CLAIM_RECOVERY_BINDING_COMPONENTS = MappingProxyType(
    {
        "typed_replay/binding/prelaunch-projection.json": (
            "prelaunch_projection"
        ),
        "typed_replay/binding/handoff.json": "handoff",
        "typed_replay/binding/reservation.json": "reservation",
    }
)


def build_proof_claim_recovery_seed_attachments(
    *,
    prelaunch_projection: Mapping[str, Any],
    handoff: Mapping[str, Any],
    reservation: Mapping[str, Any],
) -> dict[str, bytes]:
    """Freeze the pre-claim components needed for clean-process recovery.

    The execution claim and its verified commit reference cannot exist before
    the claim commit.  They are therefore reopened from that exact commit at
    recovery time, while these three deterministic components are committed
    atomically beside the claim.  The result is inert byte evidence and cannot
    authorize launch or retry.
    """

    components = {
        "prelaunch_projection": prelaunch_projection,
        "handoff": handoff,
        "reservation": reservation,
    }
    frozen: dict[str, bytes] = {}
    for logical_name, component_name in _CLAIM_RECOVERY_BINDING_COMPONENTS.items():
        value = components[component_name]
        data = _canonical_mapping_bytes(
            value, f"proof recovery {component_name}"
        )
        decoded = _decode_mapping(data, f"proof recovery {component_name}")
        digest_field = (
            "reservation_digest"
            if component_name == "reservation"
            else "content_digest"
        )
        _require_self_digest(
            decoded,
            label=f"proof recovery {component_name}",
            field=digest_field,
        )
        frozen[logical_name] = data
    return {
        logical_name: memoryview(data).tobytes()
        for logical_name, data in sorted(frozen.items())
    }


def replay_proof_execution_claim_binding_from_recovery_bytes(
    *,
    attachment_bytes: Mapping[str, bytes],
    expected_reservation: Mapping[str, Any],
    execution_claim: Mapping[str, Any],
    execution_claim_reference: Mapping[str, Any],
) -> ProofExecutionClaimBinding:
    """Reconstruct one inert claim binding from committed recovery bytes."""

    if not isinstance(attachment_bytes, Mapping):
        raise ProofExecutionContractError(
            "proof claim recovery attachments must be an object"
        )
    if set(attachment_bytes) != set(_CLAIM_RECOVERY_BINDING_COMPONENTS):
        raise ProofExecutionContractError(
            "proof claim recovery attachment coverage is not exact"
        )
    decoded = {
        component_name: _decode_mapping(
            _replay_bytes(attachment_bytes, logical_name),
            f"proof recovery {component_name}",
        )
        for logical_name, component_name in _CLAIM_RECOVERY_BINDING_COMPONENTS.items()
    }
    if decoded["reservation"] != dict(expected_reservation):
        raise ProofExecutionContractError(
            "proof claim recovery crossed its durable reservation"
        )
    return build_proof_execution_claim_binding(
        prelaunch_projection=decoded["prelaunch_projection"],
        handoff=decoded["handoff"],
        reservation=decoded["reservation"],
        execution_claim=execution_claim,
        execution_claim_reference=execution_claim_reference,
    )


def build_staged_proof_invocation_recovery_attachments(
    invocation: StagedProofInvocation,
) -> dict[str, bytes]:
    """Freeze the exact staged invocation before the sole launch boundary."""

    projection = validate_staged_proof_invocation(invocation)
    attachments: dict[str, bytes] = {
        _REPLAY_INVOCATION_PROJECTION: canonical_json(projection),
        _REPLAY_INVOCATION_DEPENDENCY_AUTHORITY: memoryview(
            invocation._dependency_authority_bytes
        ).tobytes(),
        _REPLAY_INVOCATION_EXECUTABLE_AUTHORITY: memoryview(
            invocation._executable_authority_bytes
        ).tobytes(),
        _REPLAY_INVOCATION_STDIN: invocation.stdin.read_bytes(),
    }
    for artifact in invocation.files:
        attachments[
            f"{_REPLAY_INVOCATION_FILE_PREFIX}{artifact.relative_path}"
        ] = artifact.read_bytes()
    return {
        logical_name: memoryview(data).tobytes()
        for logical_name, data in sorted(attachments.items())
    }


def terminal_projection_requires_launch_checkpoint(
    projection: Mapping[str, Any],
) -> bool:
    """Return whether one historical terminal shape crossed the launch boundary."""

    payload = validate_terminal_result_projection(projection)
    shape = _TERMINAL_SHAPES[payload["terminal_status"]]
    if shape.phase in {"spawn", "supervision", "protocol", "artifact", "complete"}:
        return True
    return (
        payload["terminal_status"] == "abandoned_uncertain"
        and payload["reason_code"] == "execution_outcome_unknown_abandoned"
    )


def build_proof_terminal_replay_attachments(
    terminal: ProofExecutionTerminalResult,
) -> dict[str, bytes]:
    """Freeze the private typed-construction seed and terminal evidence.

    These bytes are inert evidence.  They cannot reissue launch authority, but
    they are sufficient to reconstruct the exact binding, staged invocation,
    and terminal object after persistence.
    """

    validate_proof_execution_terminal_result(terminal)
    binding = terminal.claim_binding
    attachments = _terminal_attachment_bytes(terminal)
    for logical_name, attribute in _REPLAY_BINDING_COMPONENTS.items():
        data = getattr(binding, attribute)
        if type(data) is not bytes:
            raise ProofExecutionContractError(
                "proof claim binding lost exact replay bytes"
            )
        attachments[logical_name] = memoryview(data).tobytes()
    attachments[_REPLAY_BINDING_PROJECTION] = canonical_json(
        validate_proof_execution_claim_binding(binding)
    )

    invocation = terminal.invocation
    if invocation is not None:
        attachments.update(
            build_staged_proof_invocation_recovery_attachments(invocation)
        )
    return {
        logical_name: memoryview(data).tobytes()
        for logical_name, data in sorted(attachments.items())
    }


def _replay_bytes(
    attachments: Mapping[str, bytes],
    logical_name: str,
) -> bytes:
    try:
        data = attachments[logical_name]
    except KeyError as exc:
        raise ProofExecutionContractError(
            f"durable terminal replay lacks {logical_name!r}"
        ) from exc
    if type(data) is not bytes:
        raise ProofExecutionContractError(
            f"durable terminal replay attachment {logical_name!r} "
            "must be exact bytes"
        )
    return memoryview(data).tobytes()


def _artifact_from_replay_descriptor(
    descriptor: Mapping[str, Any],
    data: bytes,
    *,
    label: str,
) -> StagedByteArtifact:
    _require_exact_keys(
        descriptor,
        frozenset(
            {
                "relative_path",
                "roles",
                "sha256",
                "byte_length",
                "executable",
            }
        ),
        label,
    )
    roles = descriptor["roles"]
    if not isinstance(roles, list):
        raise ProofExecutionContractError(f"{label} roles must be an array")
    artifact = StagedByteArtifact.from_bytes(
        descriptor["relative_path"],
        data,
        roles=roles,
        executable=descriptor["executable"],
    )
    if artifact.descriptor() != dict(descriptor):
        raise ProofExecutionContractError(
            f"{label} bytes differ from their durable descriptor"
        )
    return artifact


def replay_staged_proof_invocation_from_recovery_bytes(
    binding: ProofExecutionClaimBinding,
    *,
    attachment_bytes: Mapping[str, bytes],
) -> StagedProofInvocation:
    """Reconstruct the inert staged invocation persisted at checkpoint CAS."""

    binding_projection = validate_proof_execution_claim_binding(binding)
    if not isinstance(attachment_bytes, Mapping):
        raise ProofExecutionContractError(
            "proof invocation recovery attachments must be an object"
        )
    attachments = {
        str(name): _replay_bytes(attachment_bytes, str(name))
        for name in attachment_bytes
    }
    invocation_projection = validate_staged_invocation_projection(
        _decode_mapping(
            _replay_bytes(attachments, _REPLAY_INVOCATION_PROJECTION),
            "durable staged invocation projection",
        ),
        expected_binding_digest=binding_projection["content_digest"],
    )
    expected_names = {
        _REPLAY_INVOCATION_PROJECTION,
        _REPLAY_INVOCATION_DEPENDENCY_AUTHORITY,
        _REPLAY_INVOCATION_EXECUTABLE_AUTHORITY,
        _REPLAY_INVOCATION_STDIN,
    }
    stdin = _artifact_from_replay_descriptor(
        invocation_projection["stdin"],
        _replay_bytes(attachments, _REPLAY_INVOCATION_STDIN),
        label="durable staged stdin",
    )
    files: list[StagedByteArtifact] = []
    for descriptor in invocation_projection["files"]:
        if not isinstance(descriptor, Mapping):
            raise ProofExecutionContractError(
                "durable staged file descriptor must be an object"
            )
        logical_name = (
            f"{_REPLAY_INVOCATION_FILE_PREFIX}"
            f"{descriptor.get('relative_path', '')}"
        )
        expected_names.add(logical_name)
        files.append(
            _artifact_from_replay_descriptor(
                descriptor,
                _replay_bytes(attachments, logical_name),
                label="durable staged file",
            )
        )
    if set(attachments) != expected_names:
        raise ProofExecutionContractError(
            "proof invocation recovery attachment coverage is not exact"
        )
    invocation = StagedProofInvocation(
        claim_binding=binding,
        runtime_route=resolve_proof_runtime_route(
            binding_projection["proof_adapter"]
        ),
        stdin=stdin,
        files=tuple(files),
        logical_argv=tuple(invocation_projection["logical_argv"]),
        materialized_argv=tuple(invocation_projection["materialized_argv"]),
        artifact_policy=invocation_projection["artifact_policy"],
        _dependency_authority_bytes=_replay_bytes(
            attachments,
            _REPLAY_INVOCATION_DEPENDENCY_AUTHORITY,
        ),
        _executable_authority_bytes=_replay_bytes(
            attachments,
            _REPLAY_INVOCATION_EXECUTABLE_AUTHORITY,
        ),
    )
    if validate_staged_proof_invocation(invocation) != invocation_projection:
        raise ProofExecutionContractError(
            "proof invocation recovery changed its exact projection"
        )
    return invocation


def replay_proof_terminal_from_durable_bytes(
    terminal_projection: Mapping[str, Any],
    *,
    attachment_bytes: Mapping[str, bytes],
    expected_reservation: Mapping[str, Any],
    expected_execution_claim: Mapping[str, Any],
    expected_launch_checkpoint: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Reconstruct and validate the full typed terminal contract.

    The reservation, claim, and checkpoint parameters must be records reopened
    by the coordination ledger.  Caller-authored serialized projections never
    substitute for those durable records.
    """

    payload = validate_terminal_result_projection(terminal_projection)
    if not isinstance(attachment_bytes, Mapping):
        raise ProofExecutionContractError(
            "durable terminal replay attachments must be an object"
        )
    attachments = {
        str(name): _replay_bytes(attachment_bytes, str(name))
        for name in attachment_bytes
    }
    expected_names = set(_REPLAY_BINDING_COMPONENTS)
    expected_names.add(_REPLAY_BINDING_PROJECTION)
    binding_kwargs = {
        attribute: _replay_bytes(attachments, logical_name)
        for logical_name, attribute in _REPLAY_BINDING_COMPONENTS.items()
    }
    binding = ProofExecutionClaimBinding(**binding_kwargs)
    binding_projection = validate_proof_execution_claim_binding(binding)
    if (
        _replay_bytes(attachments, _REPLAY_BINDING_PROJECTION)
        != canonical_json(binding_projection)
        or binding.reservation != dict(expected_reservation)
        or binding.execution_claim != dict(expected_execution_claim)
        or payload["binding_id"] != binding_projection["binding_id"]
        or payload["binding_digest"] != binding_projection["content_digest"]
    ):
        raise ProofExecutionContractError(
            "durable terminal replay crossed its exact claim binding"
        )

    invocation: StagedProofInvocation | None = None
    invocation_projection: dict[str, Any] | None = None
    if payload["invocation_id"] is not None:
        expected_names.update(
            {
                _REPLAY_INVOCATION_PROJECTION,
                _REPLAY_INVOCATION_DEPENDENCY_AUTHORITY,
                _REPLAY_INVOCATION_EXECUTABLE_AUTHORITY,
                _REPLAY_INVOCATION_STDIN,
            }
        )
        invocation_projection = validate_staged_invocation_projection(
            _decode_mapping(
                _replay_bytes(attachments, _REPLAY_INVOCATION_PROJECTION),
                "durable staged invocation projection",
            ),
            expected_binding_digest=binding_projection["content_digest"],
        )
        stdin = _artifact_from_replay_descriptor(
            invocation_projection["stdin"],
            _replay_bytes(attachments, _REPLAY_INVOCATION_STDIN),
            label="durable staged stdin",
        )
        files: list[StagedByteArtifact] = []
        for descriptor in invocation_projection["files"]:
            if not isinstance(descriptor, Mapping):
                raise ProofExecutionContractError(
                    "durable staged file descriptor must be an object"
                )
            logical_name = (
                f"{_REPLAY_INVOCATION_FILE_PREFIX}"
                f"{descriptor.get('relative_path', '')}"
            )
            expected_names.add(logical_name)
            files.append(
                _artifact_from_replay_descriptor(
                    descriptor,
                    _replay_bytes(attachments, logical_name),
                    label="durable staged file",
                )
            )
        invocation = StagedProofInvocation(
            claim_binding=binding,
            runtime_route=resolve_proof_runtime_route(
                binding_projection["proof_adapter"]
            ),
            stdin=stdin,
            files=tuple(files),
            logical_argv=tuple(invocation_projection["logical_argv"]),
            materialized_argv=tuple(
                invocation_projection["materialized_argv"]
            ),
            artifact_policy=invocation_projection["artifact_policy"],
            _dependency_authority_bytes=_replay_bytes(
                attachments,
                _REPLAY_INVOCATION_DEPENDENCY_AUTHORITY,
            ),
            _executable_authority_bytes=_replay_bytes(
                attachments,
                _REPLAY_INVOCATION_EXECUTABLE_AUTHORITY,
            ),
        )
        reconstructed_invocation = validate_staged_proof_invocation(
            invocation
        )
        if (
            reconstructed_invocation != invocation_projection
            or payload["invocation_id"] != invocation_projection["invocation_id"]
            or payload["invocation_digest"]
            != invocation_projection["content_digest"]
        ):
            raise ProofExecutionContractError(
                "durable terminal replay crossed its exact staged invocation"
            )
    elif payload["invocation_digest"] is not None:
        raise ProofExecutionContractError(
            "durable terminal replay has an invocation digest without an invocation"
        )

    process_event: dict[str, Any] | None = None
    if payload["process_event"] is not None:
        expected_names.add("process_event")
        process_event = _decode_mapping(
            _replay_bytes(attachments, "process_event"),
            "durable proof process event",
        )
        if process_event != payload["process_event"]:
            raise ProofExecutionContractError(
                "durable process bytes differ from the terminal projection"
            )
    resource_receipt: dict[str, Any] | None = None
    if payload["resource_receipt"] is not None:
        expected_names.add("resource_receipt")
        resource_receipt = _decode_mapping(
            _replay_bytes(attachments, "resource_receipt"),
            "durable proof resource receipt",
        )
        if resource_receipt != payload["resource_receipt"]:
            raise ProofExecutionContractError(
                "durable resource bytes differ from the terminal projection"
            )
    checker_output: bytes | None = None
    if payload["checker_output"] is not None:
        expected_names.add("checker_output")
        checker_output = _replay_bytes(attachments, "checker_output")
        if (
            bytes_digest(checker_output) != payload["checker_output"]["sha256"]
            or len(checker_output) != payload["checker_output"]["byte_length"]
        ):
            raise ProofExecutionContractError(
                "durable checker bytes differ from the terminal projection"
            )
    certificate: dict[str, Any] | None = None
    if payload["certificate"] is not None:
        expected_names.add("certificate")
        certificate = _decode_mapping(
            _replay_bytes(attachments, "certificate"),
            "durable proof certificate",
        )
        if certificate != payload["certificate"]:
            raise ProofExecutionContractError(
                "durable certificate bytes differ from the terminal projection"
            )
    artifacts: list[StagedByteArtifact] = []
    for descriptor in payload["artifacts"]:
        if not isinstance(descriptor, Mapping):
            raise ProofExecutionContractError(
                "durable result-artifact descriptor must be an object"
            )
        logical_name = f"result_artifact/{descriptor.get('relative_path', '')}"
        expected_names.add(logical_name)
        artifacts.append(
            _artifact_from_replay_descriptor(
                descriptor,
                _replay_bytes(attachments, logical_name),
                label="durable result artifact",
            )
        )

    checkpoint_required = terminal_projection_requires_launch_checkpoint(
        payload
    )
    if expected_launch_checkpoint is None:
        if checkpoint_required:
            raise ProofExecutionContractError(
                "launch-or-later proof terminal lacks its durable checkpoint"
            )
    else:
        if invocation_projection is None:
            raise ProofExecutionContractError(
                "durable launch checkpoint lacks its exact staged invocation"
            )
        expected_names.add(TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT)
        checkpoint_bytes = _replay_bytes(
            attachments, TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT
        )
        checkpoint = _decode_mapping(
            checkpoint_bytes, "durable proof launch checkpoint"
        )
        if (
            checkpoint != dict(expected_launch_checkpoint)
            or checkpoint_bytes
            != canonical_json(dict(expected_launch_checkpoint))
            or checkpoint.get("binding_id") != binding_projection["binding_id"]
            or checkpoint.get("binding_digest")
            != binding_projection["content_digest"]
            or checkpoint.get("invocation_id")
            != invocation_projection["invocation_id"]
            or checkpoint.get("invocation_digest")
            != invocation_projection["content_digest"]
            or checkpoint.get("execution_claim_id")
            != expected_execution_claim.get("execution_claim_id")
            or checkpoint.get("execution_claim_digest")
            != expected_execution_claim.get("execution_claim_digest")
        ):
            raise ProofExecutionContractError(
                "durable launch checkpoint crossed its binding or invocation"
            )

    if set(attachments) != expected_names:
        raise ProofExecutionContractError(
            "durable terminal replay attachment coverage is not exact"
        )
    reconstructed = build_proof_execution_terminal_result(
        binding,
        terminal_status=payload["terminal_status"],
        execution_status=payload["execution_status"],
        proof_verdict=payload["proof_verdict"],
        reason_code=payload["reason_code"],
        started_at=payload["started_at"],
        completed_at=payload["completed_at"],
        invocation=invocation,
        process_event=process_event,
        resource_receipt=resource_receipt,
        checker_output=checker_output,
        certificate=certificate,
        artifacts=artifacts,
    )
    replayed = validate_proof_execution_terminal_result(reconstructed)
    if replayed != payload:
        raise ProofExecutionContractError(
            "durable bytes do not reconstruct the exact terminal projection"
        )
    return replayed


_TERMINAL_PROJECTION_KEYS = frozenset(
    {
        "schema_version",
        "contract_version",
        "terminal_kind",
        "binding_id",
        "binding_digest",
        "execution_claim_id",
        "execution_claim_digest",
        "reservation_id",
        "reservation_digest",
        "attempt_id",
        "attempt_number",
        "handoff_id",
        "handoff_digest",
        "formal_claim_digest",
        "invocation_id",
        "invocation_digest",
        "terminal_status",
        "terminal_phase",
        "launch_disposition",
        "execution_status",
        "proof_verdict",
        "reason_code",
        "started_at",
        "completed_at",
        "process_event",
        "process_event_digest",
        "resource_receipt",
        "resource_receipt_digest",
        "checker_output",
        "certificate",
        "certificate_digest",
        "artifacts",
        "epistemic_effect",
        "persisted",
        "authoritative_for_atomic_finalization",
        "pending_n_plus_one_reflection_created",
        "same_cycle_theory_mutation",
        "authority_nulls",
        "terminal_id",
        "content_digest",
    }
)


def validate_terminal_result_projection(
    projection: Mapping[str, Any],
    *,
    expected_binding_digest: str | None = None,
) -> dict[str, Any]:
    """Decode inert historical evidence without finalizing a current ledger."""

    payload = _decode_mapping(
        _canonical_mapping_bytes(projection, "proof terminal projection"),
        "proof terminal projection",
    )
    _require_exact_keys(payload, _TERMINAL_PROJECTION_KEYS, "proof terminal")
    _require_self_digest(payload, label="proof terminal")
    if (
        payload["schema_version"] != 1
        or payload["contract_version"] != TERMINAL_RESULT_CONTRACT_VERSION
        or payload["terminal_kind"]
        != "total_proof_execution_operational_result"
        or payload["persisted"] is not False
        or payload["authoritative_for_atomic_finalization"] is not False
        or payload["pending_n_plus_one_reflection_created"] is not False
        or payload["same_cycle_theory_mutation"] is not False
        or payload["epistemic_effect"]
        != "none_operational_result_pending_distinct_n_plus_one_intake"
    ):
        raise ProofExecutionContractError(
            "terminal projection overstates persistence or epistemic authority"
        )
    _validate_authority_nulls(
        payload["authority_nulls"], "proof terminal projection"
    )
    if payload["terminal_status"] not in _TERMINAL_SHAPES:
        raise ProofExecutionContractError(
            "terminal projection has an unregistered status"
        )
    if payload["proof_verdict"] not in TERMINAL_PROOF_VERDICTS:
        raise ProofExecutionContractError(
            "terminal projection has an unregistered proof verdict"
        )
    if (
        expected_binding_digest is not None
        and payload["binding_digest"] != expected_binding_digest
    ):
        raise ProofExecutionContractError(
            "terminal projection crossed its claim binding"
        )
    _validated_utc_seconds(payload["started_at"], "terminal started_at")
    _validated_utc_seconds(payload["completed_at"], "terminal completed_at")
    return payload


def _current_builtin_dependency_profile() -> ProofDependencyProfile:
    """Return the closed repository-local profile for the v3 built-in worker."""

    return ProofDependencyProfile.from_mappings(
        scope="current-proof-builtin-worker-v3",
        entry_python_paths={
            _CURRENT_WORKER_RELATIVE_PATH: (
                "builtin_worker_entrypoint",
                "proof_protocol_implementation",
            )
        },
        semantic_paths={
            _CURRENT_WORKER_RELATIVE_PATH: (
                "proof_protocol_semantics",
            )
        },
        authority_boundary=(
            "complete_recursive_repository_python_and_semantic_closure_for_the_"
            "stdlib_only_builtin_worker;_the_separately_bound_python_executable_"
            "records_unavailable_host_stdlib_and_shared_library_byte_remainder"
        ),
    )


def _safe_absolute_regular_file_bytes(
    raw_path: Path | str,
) -> tuple[Path, bytes, os.stat_result]:
    """Capture one canonical absolute regular file without following symlinks."""

    path = Path(raw_path)
    if not path.is_absolute():
        raise ProofExecutionContractError(
            "proof executable source path must be absolute"
        )
    cursor = Path(path.anchor)
    for part in path.parts[1:]:
        cursor = cursor / part
        metadata = os.lstat(cursor)
        if stat.S_ISLNK(metadata.st_mode):
            raise ProofExecutionContractError(
                "proof executable source path traverses a symlink"
            )
    resolved = path.resolve(strict=True)
    if resolved != path:
        raise ProofExecutionContractError(
            "proof executable source path is not canonical"
        )
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or not bool(before.st_mode & 0o111)
            or before.st_size <= 0
            or before.st_size > MAX_STAGED_FILE_BYTES
        ):
            raise ProofExecutionContractError(
                "proof executable source is not one bounded linked executable"
            )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                raise ProofExecutionContractError(
                    "proof executable source ended before its recorded size"
                )
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise ProofExecutionContractError(
                "proof executable source grew during capture"
            )
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = lambda value: (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
    )
    if identity(before) != identity(after):
        raise ProofExecutionContractError(
            "proof executable source changed during capture"
        )
    return path, b"".join(chunks), after


def _current_python_executable_artifact(
) -> tuple[StagedByteArtifact, dict[str, Any]]:
    """Capture the exact current interpreter and type the unclosed host remainder."""

    source = Path(sys.executable).resolve(strict=True)
    source, content, metadata = _safe_absolute_regular_file_bytes(source)
    artifact = StagedByteArtifact.from_bytes(
        "executables/python",
        content,
        roles=("python_runtime",),
        executable=True,
    )
    authority: dict[str, Any] = {
        "authority_version": "1.0.0",
        "authority_kind": "current_process_python_executable_bytes",
        "source_path": source.as_posix(),
        "staged_relative_path": artifact.relative_path,
        "sha256": artifact.content_digest,
        "byte_length": artifact.byte_length,
        "source_mode": metadata.st_mode,
        "source_device": metadata.st_dev,
        "source_inode": metadata.st_ino,
        "source_mtime_ns": metadata.st_mtime_ns,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform_system": platform.system(),
        "platform_machine": platform.machine(),
        "stdlib_byte_closure_complete": False,
        "shared_library_byte_closure_complete": False,
        "host_runtime_closure_status": "unavailable_unhashed_remainder",
        "ambient_path_resolution_allowed": False,
        "authority_boundary": (
            "exact_current_interpreter_file_bytes_only;_host_standard_library_"
            "and_dynamic_shared_library_byte_closure_remain_explicitly_unavailable"
        ),
    }
    authority["content_digest"] = _self_digest(authority)
    return artifact, _validate_executable_authority_projection(authority)


def _directory_open_flags() -> int:
    return (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _open_child_directory(parent_fd: int, name: str) -> int:
    descriptor = os.open(name, _directory_open_flags(), dir_fd=parent_fd)
    metadata = os.fstat(descriptor)
    if not stat.S_ISDIR(metadata.st_mode):
        os.close(descriptor)
        raise ProofExecutionContractError(
            "proof runtime path component is not a directory"
        )
    return descriptor


def _create_runtime_root(
    coordination_run_root: Path,
    proof_runtime_ref: str,
) -> tuple[Path, int]:
    """Create the claim-bound attempt root through anchored no-follow dirfds."""

    base = Path(coordination_run_root)
    if base.is_symlink() or not base.is_dir():
        raise ProofExecutionContractError(
            "coordination run root is not a canonical directory"
        )
    base = base.resolve(strict=True)
    relative = _validated_relative_path(
        proof_runtime_ref, "proof runtime reference"
    )
    parts = Path(relative).parts
    base_fd = os.open(base, _directory_open_flags())
    current_fd = base_fd
    try:
        for index, part in enumerate(parts):
            final = index == len(parts) - 1
            try:
                os.mkdir(part, mode=0o700, dir_fd=current_fd)
            except FileExistsError:
                if final:
                    raise ProofExecutionContractError(
                        "claimed proof runtime root already exists; respawn is forbidden"
                    ) from None
            child_fd = _open_child_directory(current_fd, part)
            if current_fd != base_fd:
                os.close(current_fd)
            current_fd = child_fd
        runtime_root = base.joinpath(*parts)
        if runtime_root.resolve(strict=True) != runtime_root:
            raise ProofExecutionContractError(
                "proof runtime root is not canonical"
            )
        return runtime_root, current_fd
    except Exception:
        if current_fd != base_fd:
            os.close(current_fd)
        raise
    finally:
        os.close(base_fd)


def _directory_for_artifact(root_fd: int, parts: tuple[str, ...]) -> int:
    current_fd = os.dup(root_fd)
    try:
        for part in parts:
            try:
                os.mkdir(part, mode=0o700, dir_fd=current_fd)
            except FileExistsError:
                pass
            child_fd = _open_child_directory(current_fd, part)
            os.close(current_fd)
            current_fd = child_fd
        return current_fd
    except Exception:
        os.close(current_fd)
        raise


def _read_regular_at(parent_fd: int, leaf: str) -> tuple[bytes, os.stat_result]:
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(leaf, flags, dir_fd=parent_fd)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise ProofExecutionContractError(
                "materialized proof artifact is not one regular file"
            )
        chunks: list[bytes] = []
        remaining = metadata.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                raise ProofExecutionContractError(
                    "materialized proof artifact ended before its stated size"
                )
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise ProofExecutionContractError(
                "materialized proof artifact grew during verification"
            )
        after = os.fstat(descriptor)
        if (
            metadata.st_dev,
            metadata.st_ino,
            metadata.st_mode,
            metadata.st_nlink,
            metadata.st_size,
            metadata.st_mtime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_mode,
            after.st_nlink,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise ProofExecutionContractError(
                "materialized proof artifact changed during verification"
            )
        return b"".join(chunks), after
    finally:
        os.close(descriptor)


def _materialize_artifact(root_fd: int, artifact: StagedByteArtifact) -> None:
    parts = Path(artifact.relative_path).parts
    parent_fd = _directory_for_artifact(root_fd, parts[:-1])
    try:
        flags = (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(
            parts[-1],
            flags,
            0o700 if artifact.executable else 0o600,
            dir_fd=parent_fd,
        )
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise ProofExecutionContractError(
                    "new proof artifact is not one regular file"
                )
            view = memoryview(artifact.content)
            written = 0
            while written < len(view):
                count = os.write(descriptor, view[written:])
                if count <= 0:
                    raise ProofExecutionContractError(
                        "proof artifact write made no progress"
                    )
                written += count
            os.fchmod(descriptor, 0o700 if artifact.executable else 0o600)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        observed, observed_metadata = _read_regular_at(parent_fd, parts[-1])
        if (
            observed != artifact.content
            or bytes_digest(observed) != artifact.content_digest
            or len(observed) != artifact.byte_length
            or bool(observed_metadata.st_mode & 0o111) is not artifact.executable
        ):
            raise ProofExecutionContractError(
                "materialized proof artifact differs from exact staged bytes"
            )
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def _verify_materialized_artifact(
    root_fd: int, artifact: StagedByteArtifact
) -> None:
    parts = Path(artifact.relative_path).parts
    parent_fd = _directory_for_artifact(root_fd, parts[:-1])
    try:
        content, metadata = _read_regular_at(parent_fd, parts[-1])
    finally:
        os.close(parent_fd)
    if (
        content != artifact.content
        or bytes_digest(content) != artifact.content_digest
        or len(content) != artifact.byte_length
        or bool(metadata.st_mode & 0o111) is not artifact.executable
    ):
        raise ProofExecutionContractError(
            "staged proof bytes changed before governed spawn"
        )


def _stage_current_builtin_invocation(
    binding: ProofExecutionClaimBinding,
    *,
    runtime_root: Path,
    runtime_fd: int,
) -> tuple[
    StagedProofInvocation,
    ProofDependencyProfile,
    dict[str, Any],
]:
    profile = _current_builtin_dependency_profile()
    authority = profile.build_authority(repository_root=ROOT)
    dependencies = capture_dependency_artifacts(
        profile, authority, repository_root=ROOT
    )
    executable, executable_authority = _current_python_executable_artifact()
    invocation = build_staged_proof_invocation(
        binding,
        dependency_profile=profile,
        dependency_authority=authority,
        files=(*dependencies, executable),
        materialized_runtime_root=runtime_root,
        executable_authority=executable_authority,
        repository_root=ROOT,
    )
    for artifact in (invocation.stdin, *invocation.files):
        _materialize_artifact(runtime_fd, artifact)
    temporary_fd = _directory_for_artifact(runtime_fd, ("tmp",))
    os.close(temporary_fd)
    return invocation, profile, authority


def _revalidate_pre_spawn_authority(
    invocation: StagedProofInvocation,
    *,
    profile: ProofDependencyProfile,
    dependency_authority: Mapping[str, Any],
    runtime_fd: int,
) -> None:
    expected_dependencies = capture_dependency_artifacts(
        profile, dependency_authority, repository_root=ROOT
    )
    staged_dependencies = tuple(
        artifact
        for artifact in invocation.files
        if "dependency" in artifact.roles
    )
    if expected_dependencies != staged_dependencies:
        raise ProofExecutionContractError(
            "proof dependency bytes changed immediately before spawn"
        )
    executable = next(
        artifact
        for artifact in invocation.files
        if "python_runtime" in artifact.roles
    )
    fresh_executable, fresh_authority = _current_python_executable_artifact()
    if (
        fresh_executable != executable
        or fresh_authority != dict(invocation.executable_authority)
    ):
        raise ProofExecutionContractError(
            "proof executable authority changed immediately before spawn"
        )
    for artifact in (invocation.stdin, *invocation.files):
        _verify_materialized_artifact(runtime_fd, artifact)


def _terminal_attachment_bytes(
    terminal: ProofExecutionTerminalResult,
) -> dict[str, bytes]:
    attachments: dict[str, bytes] = {}
    if terminal.process_event is not None:
        attachments["process_event"] = canonical_json(terminal.process_event)
    if terminal.resource_receipt is not None:
        attachments["resource_receipt"] = canonical_json(
            terminal.resource_receipt
        )
    if terminal.checker_output is not None:
        attachments["checker_output"] = terminal.checker_output
    if terminal.certificate is not None:
        attachments["certificate"] = canonical_json(terminal.certificate)
    for artifact in terminal.artifacts:
        attachments[
            f"result_artifact/{artifact.relative_path}"
        ] = artifact.read_bytes()
    return attachments


def _resource_receipt_after_process(
    governor: ResourceGovernor,
    status: str,
) -> dict[str, Any]:
    """Return the exact governor receipt even if its projection method raises.

    The fallback reads only the governor's already-observed typed state and is
    byte-for-byte the same mapping as ``ResourceGovernor.receipt``.  It neither
    reruns the process nor invents a missing measurement.
    """

    try:
        return governor.receipt(status)
    except Exception:
        if status not in GOVERNOR_TERMINAL_STATUSES:
            raise
        return {
            "budget": dataclasses.asdict(governor.budget),
            "usage": dataclasses.asdict(governor.usage),
            "status": status,
            "events": list(governor.events),
            "deadline": governor.deadline.isoformat(),
            "resource_measurement": governor.measurement_boundaries(),
        }


def _finalize_terminal(
    coordination_ledger: Any,
    terminal: ProofExecutionTerminalResult,
) -> ProofExecutionTerminalResult:
    """Commit and reopen the terminal bundle before exposing the result."""

    projection = validate_proof_execution_terminal_result(terminal)
    committed = None
    first_error: Exception | None = None
    try:
        committed = coordination_ledger.finalize_proof_execution(terminal)
    except Exception as exc:
        first_error = exc
        try:
            reopened_after_uncertainty = (
                coordination_ledger.read_proof_terminal_bundle(
                    projection["reservation_id"]
                )
            )
        except Exception:
            reopened_after_uncertainty = None
        if (
            reopened_after_uncertainty is not None
            and dict(reopened_after_uncertainty.record).get(
                "terminal_projection"
            )
            == projection
        ):
            committed = reopened_after_uncertainty
        else:
            # The exact retry is idempotent.  It can finish a failure known to
            # precede commit or reopen an uncertain post-rename commit; it can
            # never authorize another proof process.
            try:
                committed = coordination_ledger.finalize_proof_execution(
                    terminal
                )
            except Exception:
                raise first_error
    assert committed is not None
    reopened = coordination_ledger.read_proof_terminal_bundle(
        projection["reservation_id"]
    )
    committed_record = dict(committed.record)
    reopened_record = dict(reopened.record)
    if (
        committed_record != reopened_record
        or reopened_record.get("terminal_projection") != projection
        or reopened_record.get("terminal_projection_digest")
        != projection["content_digest"]
        or reopened_record.get("lifecycle_terminalization", {}).get(
            "respawn_authorized"
        )
        is not False
    ):
        raise ProofExecutionContractError(
            "durably reopened proof terminal differs from the exact result"
        )
    object.__setattr__(
        terminal,
        "_durable_bundle_bytes",
        canonical_json(reopened_record),
    )
    object.__setattr__(
        terminal,
        "_durable_commit_reference_bytes",
        canonical_json(dict(reopened.ledger_commit_reference)),
    )
    return terminal


def _terminal_after_staging_failure(
    coordination_ledger: Any,
    binding: ProofExecutionClaimBinding,
    *,
    started_at: str,
    reason_code: str,
) -> ProofExecutionTerminalResult:
    return _finalize_terminal(
        coordination_ledger,
        build_staging_rejection_terminal(
            binding,
            reason_code=reason_code,
            observed_at=started_at,
        ),
    )


def _execute_current_proof_v3(
    capability: "ProofPrelaunchCapability",
) -> ProofExecutionTerminalResult:
    """Consume and execute one exact live proof capability, then finalize it.

    This is the sole launch entrypoint.  It accepts no command, path, attempt,
    dependency, environment, callback, failpoint, plan, retry, or handoff
    parameter.  Failures before the durable claim propagate because no valid
    terminal binding exists; every phase after a returned claim is converted
    to one terminal result and finalized before return.
    """

    from .proof import (
        ProofPrelaunchCapability,
        _consume_proof_prelaunch_capability,
    )

    if type(capability) is not ProofPrelaunchCapability:
        raise ProofExecutionContractError(
            "current proof execution requires one exact live prelaunch capability"
        )
    coordination_ledger = capability._coordination_ledger
    (
        prelaunch,
        handoff,
        reservation,
        execution_claim,
        execution_claim_reference,
    ) = _consume_proof_prelaunch_capability(capability)
    binding = build_proof_execution_claim_binding(
        prelaunch_projection=prelaunch,
        handoff=handoff,
        reservation=reservation,
        execution_claim=execution_claim,
        execution_claim_reference=execution_claim_reference,
    )
    started_at = _utc_now_seconds()
    binding_projection = validate_proof_execution_claim_binding(binding)
    try:
        route = resolve_proof_runtime_route(binding_projection["proof_adapter"])
    except ProofExecutionContractError:
        return _terminal_after_staging_failure(
            coordination_ledger,
            binding,
            started_at=started_at,
            reason_code="runtime_route_unregistered",
        )
    if route.adapter not in {"exact", "finite_model"}:
        return _terminal_after_staging_failure(
            coordination_ledger,
            binding,
            started_at=started_at,
            reason_code="runtime_executable_authority_unavailable",
        )

    runtime_fd: int | None = None
    try:
        try:
            runtime_root, runtime_fd = _create_runtime_root(
                coordination_ledger.coordination_run_root,
                binding_projection["proof_runtime_ref"],
            )
            invocation, profile, dependency_authority = (
                _stage_current_builtin_invocation(
                    binding,
                    runtime_root=runtime_root,
                    runtime_fd=runtime_fd,
                )
            )
        except Exception:
            return _terminal_after_staging_failure(
                coordination_ledger,
                binding,
                started_at=started_at,
                reason_code="staging_failed",
            )

        try:
            policy = invocation.claim_binding.handoff["execution_policy"]
            capture_limit = max(
                policy["stdout_limit_bytes"],
                policy["stderr_limit_bytes"],
            )
            governor = ResourceGovernor(
                invocation.resource_budget,
                run_directory=runtime_root,
                allowed_working_directory=runtime_root,
                capture_limit_bytes=capture_limit,
            )
            replacement_environment = minimal_replacement_environment(
                runtime_root, create_temporary=False
            )
        except Exception:
            terminal = build_proof_execution_terminal_result(
                binding,
                terminal_status="governor_rejected",
                execution_status="not_started",
                proof_verdict="not_evaluated",
                reason_code="resource_governor_rejected",
                started_at=started_at,
                completed_at=_utc_now_seconds(),
                invocation=invocation,
            )
            return _finalize_terminal(coordination_ledger, terminal)

        try:
            _revalidate_pre_spawn_authority(
                invocation,
                profile=profile,
                dependency_authority=dependency_authority,
                runtime_fd=runtime_fd,
            )
        except Exception:
            terminal = build_proof_execution_terminal_result(
                binding,
                terminal_status="governor_rejected",
                execution_status="not_started",
                proof_verdict="not_evaluated",
                reason_code="pre_spawn_authority_rejected",
                started_at=started_at,
                completed_at=_utc_now_seconds(),
                invocation=invocation,
            )
            return _finalize_terminal(coordination_ledger, terminal)

        try:
            coordination_ledger.record_proof_launch_boundary_checkpoint(
                binding=binding,
                invocation=invocation,
            )
        except Exception:
            recovery = coordination_ledger.read_proof_terminal_recovery_state(
                binding_projection["reservation_id"]
            )
            if recovery["abandonment_finalization_authorized"] is True:
                observed_at = _utc_now_seconds()
                reason_code = recovery[
                    "selected_abandonment_reason_code"
                ]
                terminal = build_proof_execution_terminal_result(
                    binding,
                    terminal_status="abandoned_uncertain",
                    execution_status="uncertain",
                    proof_verdict="not_evaluated",
                    reason_code=reason_code,
                    started_at=observed_at,
                    completed_at=observed_at,
                    invocation=(
                        invocation
                        if reason_code
                        == "execution_outcome_unknown_abandoned"
                        else None
                    ),
                )
            else:
                terminal = build_proof_execution_terminal_result(
                    binding,
                    terminal_status="governor_rejected",
                    execution_status="not_started",
                    proof_verdict="not_evaluated",
                    reason_code="launch_boundary_checkpoint_rejected",
                    started_at=started_at,
                    completed_at=_utc_now_seconds(),
                    invocation=invocation,
                )
            return _finalize_terminal(coordination_ledger, terminal)

        try:
            process_event = governor.run_process(
                invocation.materialized_argv,
                cwd=runtime_root,
                replacement_environment=replacement_environment,
                role="solver",
                input_bytes=invocation.stdin.content,
                input_limit_bytes=policy["input_limit_bytes"],
                stdout_limit_bytes=policy["stdout_limit_bytes"],
                stderr_limit_bytes=policy["stderr_limit_bytes"],
            )
        except Exception:
            terminal = build_proof_execution_terminal_result(
                binding,
                terminal_status="spawn_failed",
                execution_status="not_started",
                proof_verdict="not_evaluated",
                reason_code="governed_spawn_raised",
                started_at=started_at,
                completed_at=_utc_now_seconds(),
                invocation=invocation,
            )
            return _finalize_terminal(coordination_ledger, terminal)

        status = str(process_event.get("status", "worker_failed"))
        resource_receipt = _resource_receipt_after_process(governor, status)
        if status != "succeeded":
            terminal = build_proof_execution_terminal_result(
                binding,
                terminal_status=(
                    "governed_not_started"
                    if process_event.get("pid") is None
                    else "process_failed"
                ),
                execution_status=status,
                proof_verdict="not_evaluated",
                reason_code="governed_process_failed",
                started_at=started_at,
                completed_at=_utc_now_seconds(),
                invocation=invocation,
                process_event=process_event,
                resource_receipt=resource_receipt,
            )
            return _finalize_terminal(coordination_ledger, terminal)

        try:
            _revalidate_pre_spawn_authority(
                invocation,
                profile=profile,
                dependency_authority=dependency_authority,
                runtime_fd=runtime_fd,
            )
        except Exception:
            # Preserve the already observed process/resource evidence while
            # withholding every claim verdict.  Empty checker bytes cannot
            # match the non-empty worker response and therefore force the
            # protocol-rejected shape through its exact linkage checks.
            terminal = build_proof_execution_terminal_result(
                binding,
                terminal_status="protocol_rejected",
                execution_status="succeeded",
                proof_verdict="not_evaluated",
                reason_code="post_spawn_authority_rejected",
                started_at=started_at,
                completed_at=_utc_now_seconds(),
                invocation=invocation,
                process_event=process_event,
                resource_receipt=resource_receipt,
                checker_output=b"",
            )
            return _finalize_terminal(coordination_ledger, terminal)

        checker_output: bytes
        try:
            expected_environment = complete_governed_process_environment(
                replacement_environment,
                deadline=resource_receipt["deadline"],
                budget=resource_receipt["budget"],
            )
            attempt = validate_v2_process_event(
                process_event,
                accepted=True,
                expected_workspace=runtime_root,
                expected_replacement_environment=expected_environment,
                require_live_execution_authority=True,
            )
            if attempt is None:
                raise ProofExecutionContractError(
                    "succeeded proof process lacks supervised output evidence"
                )
            checker_output = memoryview(
                attempt.stdout.retained_tail
            ).tobytes()
        except Exception:
            checker_output = b""

        try:
            raw_response = json.loads(checker_output.decode("utf-8"))
            if not isinstance(raw_response, Mapping):
                raise ProofExecutionContractError(
                    "checker response is not an object"
                )
            terminal_verdict = _CHECKER_TO_TERMINAL_VERDICT[
                str(raw_response["proof_verdict"])
            ]
            terminal = build_proof_execution_terminal_result(
                binding,
                terminal_status="completed",
                execution_status="succeeded",
                proof_verdict=terminal_verdict,
                reason_code="checker_response_accepted",
                started_at=started_at,
                completed_at=_utc_now_seconds(),
                invocation=invocation,
                process_event=process_event,
                resource_receipt=resource_receipt,
                checker_output=checker_output,
                certificate=raw_response.get("scoped_certificate"),
            )
        except (
            KeyError,
            TypeError,
            UnicodeError,
            json.JSONDecodeError,
            ProofExecutionContractError,
        ):
            terminal = build_proof_execution_terminal_result(
                binding,
                terminal_status="protocol_rejected",
                execution_status="succeeded",
                proof_verdict="not_evaluated",
                reason_code="checker_response_rejected",
                started_at=started_at,
                completed_at=_utc_now_seconds(),
                invocation=invocation,
                process_event=process_event,
                resource_receipt=resource_receipt,
                checker_output=checker_output,
            )
        return _finalize_terminal(coordination_ledger, terminal)
    finally:
        if runtime_fd is not None:
            try:
                os.close(runtime_fd)
            except OSError:
                # A finalized terminal must not be hidden by best-effort local
                # descriptor cleanup.  The descriptor grants no durable or
                # retry authority and is released by process teardown.
                pass


__all__ = [
    "CLAIM_BINDING_CONTRACT_VERSION",
    "MAX_CHECKER_OUTPUT_BYTES",
    "MAX_STAGED_FILE_BYTES",
    "MAX_STAGED_FILES",
    "MAX_STAGED_PATH_BYTES",
    "MAX_STAGED_TOTAL_BYTES",
    "PROOF_EXECUTION_AUTHORITY_NULLS",
    "ProofDependencyProfile",
    "ProofExecutionClaimBinding",
    "ProofExecutionContractError",
    "ProofExecutionTerminalResult",
    "ProofRuntimeRoute",
    "RUNTIME_REGISTRY_VERSION",
    "STAGED_INVOCATION_CONTRACT_VERSION",
    "StagedByteArtifact",
    "StagedProofInvocation",
    "TERMINAL_PROOF_VERDICTS",
    "TERMINAL_RESULT_CONTRACT_VERSION",
    "build_exact_lean_source",
    "build_proof_claim_recovery_seed_attachments",
    "build_proof_execution_claim_binding",
    "build_proof_execution_terminal_result",
    "build_proof_terminal_replay_attachments",
    "build_resource_governor_for_staged_invocation",
    "build_staged_proof_invocation_recovery_attachments",
    "build_staged_proof_invocation",
    "build_staging_rejection_terminal",
    "capture_dependency_artifacts",
    "closed_proof_runtime_registry",
    "replay_proof_execution_claim_binding_from_recovery_bytes",
    "replay_proof_terminal_from_durable_bytes",
    "replay_staged_proof_invocation_from_recovery_bytes",
    "resolve_proof_runtime_route",
    "TERMINAL_REPLAY_CHECKPOINT_ATTACHMENT",
    "terminal_projection_requires_launch_checkpoint",
    "validate_proof_execution_claim_binding",
    "validate_proof_execution_terminal_result",
    "validate_staged_invocation_projection",
    "validate_staged_proof_invocation",
    "validate_terminal_result_projection",
]
