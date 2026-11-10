# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Execute discovery operators and issue non-self-attested receipts.

An operator is executable code registered with an exact version—not a skill name
listed in prose.  The dispatcher verifies frozen inputs, executes either a Python
callable or an argv-only subprocess, runs independently registered validators,
hashes every output, and persists a receipt for success, failure, timeout, or
justified skip.  Required failures remain visible and block evaluation.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import inspect
import json
import marshal
import os
import re
import shutil
import subprocess
import tempfile
import time
import traceback
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping, Sequence

from .contracts import (
    ContractError,
    Namespace,
    bytes_digest,
    canonical_digest,
    canonical_json,
    fsync_directory,
    resolve_workspace_path,
    safe_relative_path,
    stable_identifier,
    utc_now,
    validate_digest,
    validate_identifier,
    validate_instance,
)
from .dependency_authority import (
    DependencyAuthorityError,
    capture_dependency_authority,
)


OperatorCallable = Callable[[dict[str, Any], Path], Mapping[str, Any]]
ValidatorCallable = Callable[[dict[str, Any], list[dict[str, Any]], Path], bool | None]


# Registry-owned validator dependencies use a repository-relative URI so a
# receipt generated on one checkout can be verified on another checkout.  The
# workspace remains the trust boundary for operator inputs/outputs, while this
# root is the trust boundary for local validator semantics.
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
_REPOSITORY_DEPENDENCY_PREFIX = "repo://"
_VALIDATOR_DEPENDENCY_POLICIES = {
    "declared_only",
    "derived_repository_closure_v2",
    "explicit_local_semantic_closure",
}
_DERIVED_CLOSURE_KIND = "derived_repository_closure_v2"
_CHILD_DIAGNOSTIC_MAX_CHARS = 4096
_ANSI_CONTROL_SEQUENCE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def _bounded_child_diagnostic(raw: bytes | str | None) -> str:
    """Return a readable, control-free excerpt without making logs authoritative."""

    if raw is None:
        return ""
    text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
    text = _ANSI_CONTROL_SEQUENCE.sub("", text)
    text = "".join(character if character.isprintable() else " " for character in text)
    text = " ".join(text.split())
    suffix = "...[truncated]"
    if len(text) > _CHILD_DIAGNOSTIC_MAX_CHARS:
        text = text[: _CHILD_DIAGNOSTIC_MAX_CHARS - len(suffix)] + suffix
    return text


class DispatchBlocked(ContractError):
    """Raised when required execution evidence is missing or invalid."""


def validator_dependency_policy_is_supported(authority: Mapping[str, Any]) -> bool:
    """Apply the one receipt/gate policy for bounded validator import authority.

    Legacy declared-file policies are honest only when they explicitly exclude
    undeclared transitive imports.  The derived policy instead requires exactly
    one typed recursive-closure identity.  Keeping this predicate beside receipt
    validation prevents downstream gates from accepting a shape that the generic
    receipt boundary would reject, or vice versa.
    """

    dependency_policy = authority.get("dependency_policy")
    dependency_identities = authority.get("dependency_identities", [])
    if dependency_policy in {
        "declared_only",
        "explicit_local_semantic_closure",
    }:
        excluded = authority.get("coverage", {}).get("excluded", [])
        return (
            isinstance(excluded, list)
            and "undeclared transitive imports beyond explicit dependency paths"
            in excluded
        )
    return (
        dependency_policy == _DERIVED_CLOSURE_KIND
        and isinstance(dependency_identities, list)
        and len(dependency_identities) == 1
        and isinstance(dependency_identities[0], Mapping)
        and dependency_identities[0].get("kind") == _DERIVED_CLOSURE_KIND
        and isinstance(dependency_identities[0].get("authority"), Mapping)
    )


@dataclasses.dataclass(frozen=True, slots=True)
class ValidatorDependencyProfile:
    """Typed roots for one recursively derived repository-local validator closure."""

    scope: str
    entry_python_paths: tuple[tuple[str, tuple[str, ...]], ...]
    semantic_paths: tuple[tuple[str, tuple[str, ...]], ...]
    authority_boundary: str
    runtime_distributions: tuple[tuple[str, str], ...]
    registry_path: str

    @staticmethod
    def _path_roles(value: Any, *, label: str) -> tuple[tuple[str, tuple[str, ...]], ...]:
        if not isinstance(value, Mapping) or not value:
            raise ContractError(f"{label} must be a non-empty path-to-roles object")
        rows: list[tuple[str, tuple[str, ...]]] = []
        for raw_path, raw_roles in value.items():
            if not isinstance(raw_path, str) or "\\" in raw_path:
                raise ContractError(f"{label} contains an unsafe repository path")
            path = PurePosixPath(raw_path)
            if (
                path.is_absolute()
                or path.as_posix() != raw_path
                or any(part in {"", ".", ".."} for part in path.parts)
            ):
                raise ContractError(f"{label} contains an unsafe repository path")
            if (
                not isinstance(raw_roles, list)
                or not raw_roles
                or not all(
                    isinstance(role, str) and role.strip() for role in raw_roles
                )
                or len(raw_roles) != len(set(raw_roles))
            ):
                raise ContractError(f"{label} roles are invalid for {raw_path}")
            rows.append((raw_path, tuple(sorted(raw_roles))))
        return tuple(sorted(rows))

    @classmethod
    def from_mapping(cls, value: Any) -> "ValidatorDependencyProfile":
        """Parse an exact registry profile without resolving ambient imports."""

        if not isinstance(value, Mapping):
            raise ContractError("derived validator dependency_profile must be an object")
        required = {
            "scope",
            "entry_python_paths",
            "semantic_paths",
            "authority_boundary",
            "runtime_distributions",
            "registry_path",
        }
        if set(value) != required:
            raise ContractError(
                "derived validator dependency_profile fields differ from the exact contract"
            )
        scope = value["scope"]
        boundary = value["authority_boundary"]
        registry_path = value["registry_path"]
        if not isinstance(scope, str) or not scope.strip():
            raise ContractError("derived validator dependency scope is required")
        if not isinstance(boundary, str) or len(boundary.strip()) < 8:
            raise ContractError("derived validator authority boundary is not substantive")
        if not isinstance(registry_path, str):
            raise ContractError("derived validator registry_path is invalid")
        entries = cls._path_roles(
            value["entry_python_paths"], label="entry_python_paths"
        )
        semantics = cls._path_roles(value["semantic_paths"], label="semantic_paths")
        semantic_names = {path for path, _roles in semantics}
        if registry_path not in semantic_names:
            raise ContractError(
                "derived validator registry_path must be one of the semantic roots"
            )
        distributions = value["runtime_distributions"]
        if (
            not isinstance(distributions, Mapping)
            or not distributions
            or not all(
                isinstance(module, str)
                and module.isidentifier()
                and isinstance(distribution, str)
                and distribution.strip()
                for module, distribution in distributions.items()
            )
        ):
            raise ContractError("derived validator runtime distributions are invalid")
        return cls(
            scope=scope,
            entry_python_paths=entries,
            semantic_paths=semantics,
            authority_boundary=boundary,
            runtime_distributions=tuple(sorted(distributions.items())),
            registry_path=registry_path,
        )

    def authority_arguments(self, repository_root: Path) -> dict[str, Any]:
        """Return the generic closure-builder arguments for this exact profile."""

        return {
            "scope": self.scope,
            "entry_python_paths": dict(self.entry_python_paths),
            "semantic_paths": dict(self.semantic_paths),
            "authority_boundary": self.authority_boundary,
            "repository_root": repository_root,
            "runtime_distributions": dict(self.runtime_distributions),
        }


@dataclasses.dataclass(frozen=True, slots=True)
class ValidatorBinding:
    """Independent executable validation attached to an operator binding."""

    validator_id: str
    version: str
    command: tuple[str, ...] = ()
    function: ValidatorCallable | None = None
    dependency_paths: tuple[str, ...] = ()
    dependency_policy: str = "declared_only"
    timeout_seconds: float = 60.0
    dependency_profile: ValidatorDependencyProfile | None = None
    registry_digest: str | None = None

    def __post_init__(self) -> None:
        validate_identifier(self.validator_id, "validator_id")
        validate_identifier(self.version, "validator version")
        if bool(self.command) == bool(self.function):
            raise ContractError("validator binding needs exactly one of command or function")
        if len(set(self.dependency_paths)) != len(self.dependency_paths) or not all(
            isinstance(path, str) and path.strip() for path in self.dependency_paths
        ):
            raise ContractError("validator dependency_paths must be unique non-empty paths")
        if self.dependency_policy not in _VALIDATOR_DEPENDENCY_POLICIES:
            raise ContractError(
                f"unsupported validator dependency policy: {self.dependency_policy}"
            )
        if self.dependency_policy == "explicit_local_semantic_closure" and (
            not self.dependency_paths
            or self.dependency_profile is not None
            or self.registry_digest is not None
        ):
            raise ContractError(
                "explicit validator semantic closure requires declared dependency paths"
            )
        if self.dependency_policy == "derived_repository_closure_v2":
            if (
                self.dependency_paths
                or self.dependency_profile is None
                or self.registry_digest is None
            ):
                raise ContractError(
                    "derived validator closure requires a profile and registry digest"
                )
            validate_digest(self.registry_digest)
        elif self.dependency_profile is not None or self.registry_digest is not None:
            raise ContractError(
                "validator dependency profile is only valid for a derived closure"
            )
        if self.timeout_seconds <= 0:
            raise ContractError("validator timeout must be positive")


@dataclasses.dataclass(frozen=True, slots=True)
class OperatorBinding:
    """An exact executable implementation of a named discovery capability."""

    operator_id: str
    version: str
    kind: str
    command: tuple[str, ...] = ()
    function: OperatorCallable | None = None
    validators: tuple[ValidatorBinding, ...] = ()
    timeout_seconds: float = 300.0

    def __post_init__(self) -> None:
        validate_identifier(self.operator_id, "operator_id")
        validate_identifier(self.version, "operator version")
        if self.kind not in {
            "theory",
            "literature_search",
            "literature_assimilation",
            "hypothesis",
            "proof",
            "support_probe",
            "reducer",
            "evaluation",
        }:
            raise ContractError(f"unsupported operator kind: {self.kind}")
        if bool(self.command) == bool(self.function):
            raise ContractError("operator binding needs exactly one of command or function")
        if not self.validators:
            raise ContractError("operator binding needs at least one independent validator")
        if self.timeout_seconds <= 0:
            raise ContractError("operator timeout must be positive")


def _expected_input_digest(request: Mapping[str, Any]) -> str:
    """Bind parameters and exact input descriptors into one stable digest."""

    return canonical_digest(
        {
            "identity": request["identity"],
            "operator": request["operator"],
            "parameters": request.get("parameters", {}),
            "input_artifacts": request.get("input_artifacts", []),
            "declared_outputs": request.get("declared_outputs", []),
        }
    )


def request_content_digest(request: Mapping[str, Any]) -> str:
    """Digest every request field except its two derived identity fields."""

    return canonical_digest(
        {
            key: value
            for key, value in request.items()
            if key not in {"request_id", "request_digest"}
        }
    )


def _descriptor_from_bytes(
    relative_path: str,
    data: bytes,
    namespace: Namespace,
    *,
    media_type: str | None = None,
) -> dict[str, Any]:
    """Describe the exact bytes already read, avoiding digest/stat split reads."""

    descriptor: dict[str, Any] = {
        "path": safe_relative_path(relative_path).as_posix(),
        "sha256": bytes_digest(data),
        "size_bytes": len(data),
        "namespace": namespace.as_dict(),
    }
    if media_type:
        descriptor["media_type"] = media_type
    return descriptor


def _read_verified_descriptor(
    descriptor: Mapping[str, Any], workspace: Path, namespace: Namespace
) -> tuple[Path, bytes]:
    """Read one artifact once and verify its complete descriptor from that read."""

    descriptor_namespace = Namespace.from_mapping(descriptor.get("namespace", {}))
    namespace.assert_matches(descriptor_namespace)
    path = resolve_workspace_path(workspace, str(descriptor.get("path", "")), must_exist=True)
    data = path.read_bytes()
    if bytes_digest(data) != descriptor.get("sha256"):
        raise ContractError(f"artifact digest mismatch for {descriptor.get('path')}")
    if len(data) != descriptor.get("size_bytes"):
        raise ContractError(f"artifact size mismatch for {descriptor.get('path')}")
    return path, data


def _callable_dependency_identity(name: str, value: Any) -> dict[str, Any]:
    """Name direct callable dependencies without claiming their transitive imports."""

    identity: dict[str, Any] = {"name": name}
    if inspect.ismodule(value):
        identity.update(
            {
                "kind": "module",
                "module": str(getattr(value, "__name__", "")),
                "version": str(getattr(value, "__version__", "unknown")),
            }
        )
    elif callable(value):
        target = getattr(value, "__func__", value)
        code = getattr(target, "__code__", None)
        identity.update(
            {
                "kind": "callable",
                "module": str(getattr(target, "__module__", "")),
                "qualname": str(getattr(target, "__qualname__", type(target).__qualname__)),
                "code_digest": bytes_digest(marshal.dumps(code)) if code is not None else None,
            }
        )
    else:
        identity.update(
            {
                "kind": "value",
                "type_module": type(value).__module__,
                "type_name": type(value).__qualname__,
            }
        )
        try:
            json.dumps(value, sort_keys=True, ensure_ascii=False)
        except (TypeError, ValueError):
            pass
        else:
            identity["value_digest"] = canonical_digest(value)
    return identity


def _validator_authority_material(
    binding: ValidatorBinding, workspace: Path
) -> tuple[dict[str, Any], tuple[str, ...] | None, list[tuple[dict[str, Any], bytes]]]:
    """Resolve an approved validator binding to recomputable code/file identity.

    A derived-profile binding captures its registry roots once, computes the
    recursive repository-local Python/package/schema closure from those bytes,
    and snapshots those same bytes. Legacy bindings retain their narrower
    declared-file behavior.
    """

    files: dict[Path, dict[str, Any]] = {}

    def bind_file(path: Path, role: str, data: bytes | None = None) -> None:
        resolved = path.resolve(strict=True)
        if not resolved.is_file():
            raise ContractError(f"validator authority file is not readable: {resolved}")
        row = files.setdefault(resolved, {"roles": [], "captured_data": None})
        if role not in row["roles"]:
            row["roles"].append(role)
        if data is not None:
            prior = row["captured_data"]
            if prior is not None and prior != data:
                raise ContractError(
                    f"validator dependency bytes changed during capture: {resolved}"
                )
            row["captured_data"] = data

    effective_command: tuple[str, ...] | None = None
    expected_entry: str | None = None
    if binding.command:
        raw_program = binding.command[0]
        if os.sep in raw_program:
            candidate = Path(raw_program)
            launcher = candidate if candidate.is_absolute() else workspace / candidate
        else:
            located = shutil.which(raw_program)
            if located is None:
                raise ContractError(f"validator executable is unavailable: {raw_program}")
            launcher = Path(located)
        # Execute the located launcher path itself.  In a virtual environment
        # that symlink/path controls Python's environment discovery; resolving
        # it before execution silently escapes the approved environment.  The
        # authority file binder still resolves and hashes its byte target.
        launcher = launcher.absolute()
        bind_file(launcher, "command_executable")
        effective_command = (str(launcher), *binding.command[1:])
        entry_module: str | None = None
        if len(binding.command) >= 3 and binding.command[1] == "-m":
            entry_module = binding.command[2]
            expected_entry = entry_module.replace(".", "/") + ".py"
            spec = importlib.util.find_spec(entry_module)
            if spec is None or not spec.origin or spec.origin in {"built-in", "frozen"}:
                raise ContractError(f"validator entry module has no bindable source: {entry_module}")
            if binding.dependency_policy == "derived_repository_closure_v2":
                expected_source = (
                    REPOSITORY_ROOT / safe_relative_path(expected_entry)
                ).resolve(strict=True)
                if Path(spec.origin).resolve(strict=True) != expected_source:
                    raise ContractError(
                        "validator entry module is shadowed outside the repository authority"
                    )
            bind_file(Path(spec.origin), "entry_module")
        for argument in binding.command[1:]:
            if argument.startswith("-") or argument == entry_module:
                continue
            candidate = Path(argument)
            candidate = candidate if candidate.is_absolute() else workspace / candidate
            if candidate.is_file():
                bind_file(candidate, "explicit_argument_file")
        runtime_identity: dict[str, Any] = {
            "kind": "command",
            "declared_argv": list(binding.command),
            "effective_argv": list(effective_command),
            "entry_module": entry_module,
        }
        dependency_identities: list[dict[str, Any]] = []
    else:
        function = binding.function
        target = getattr(function, "__func__", function)
        code = getattr(target, "__code__", None)
        if code is None:
            raise ContractError("validator callable has no bindable Python code object")
        source_path = inspect.getsourcefile(target) or inspect.getfile(target)
        if source_path:
            bind_file(Path(source_path), "callable_source")
        runtime_identity = {
            "kind": "callable",
            "module": str(getattr(target, "__module__", "")),
            "qualname": str(getattr(target, "__qualname__", "")),
            "code_digest": bytes_digest(marshal.dumps(code)),
            "bound_instance_type": (
                f"{type(function.__self__).__module__}.{type(function.__self__).__qualname__}"
                if inspect.ismethod(function) and function.__self__ is not None
                else None
            ),
        }
        try:
            closure = inspect.getclosurevars(target)
        except (TypeError, ValueError):
            dependency_identities = []
        else:
            dependencies = {**closure.globals, **closure.nonlocals}
            dependency_identities = [
                _callable_dependency_identity(name, dependencies[name])
                for name in sorted(dependencies)
            ]
    if binding.dependency_policy == "derived_repository_closure_v2":
        profile = binding.dependency_profile
        if profile is None or binding.registry_digest is None or expected_entry is None:
            raise ContractError("derived validator closure binding is incomplete")
        try:
            captured = capture_dependency_authority(
                **profile.authority_arguments(REPOSITORY_ROOT)
            )
        except DependencyAuthorityError as exc:
            raise ContractError(f"cannot derive validator dependency closure: {exc}") from exc
        material_map = captured.material_map()
        registry_bytes = material_map.get(profile.registry_path)
        try:
            current_registry = (
                json.loads(registry_bytes.decode("utf-8"))
                if registry_bytes is not None
                else None
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ContractError("captured validator registry is not canonical JSON") from exc
        if (
            not isinstance(current_registry, Mapping)
            or canonical_digest(current_registry) != binding.registry_digest
        ):
            raise ContractError("validator registry/current mismatch")
        closure_paths = {
            str(row["path"]) for row in captured.authority["entries"]
        }
        if expected_entry not in closure_paths:
            raise ContractError(
                "derived validator closure omits its independent validator entry module"
            )
        repository_root = REPOSITORY_ROOT.resolve()
        workspace_root = workspace.resolve()
        if workspace_root != repository_root:
            for relative in captured.authority["import_boundary"][
                "repository_local_python_paths"
            ]:
                shadow = workspace_root / safe_relative_path(relative)
                if shadow.exists() or shadow.is_symlink():
                    try:
                        same_file = shadow.resolve(strict=True) == (
                            repository_root / safe_relative_path(relative)
                        ).resolve(strict=True)
                    except OSError:
                        same_file = False
                    if not same_file:
                        raise ContractError(
                            f"validator repository import shadowing detected: {relative}"
                        )
        for row in captured.authority["entries"]:
            relative = str(row["path"])
            data = material_map[relative]
            for role in ("derived_dependency", *row["roles"]):
                bind_file(repository_root / safe_relative_path(relative), role, data)
        dependency_identities = [
            {"kind": _DERIVED_CLOSURE_KIND, "authority": captured.authority}
        ]
    else:
        for raw_path in binding.dependency_paths:
            if raw_path.startswith(_REPOSITORY_DEPENDENCY_PREFIX):
                relative = safe_relative_path(raw_path.removeprefix(_REPOSITORY_DEPENDENCY_PREFIX))
                dependency = REPOSITORY_ROOT / relative
            else:
                dependency = Path(raw_path)
                dependency = dependency if dependency.is_absolute() else workspace / dependency
            bind_file(dependency, "declared_dependency")

    materials: list[tuple[dict[str, Any], bytes]] = []
    for path, metadata in sorted(files.items(), key=lambda item: str(item[0])):
        data = metadata["captured_data"]
        if data is None:
            data = path.read_bytes()
        try:
            relative = path.relative_to(REPOSITORY_ROOT)
        except ValueError:
            try:
                relative = path.relative_to(workspace)
            except ValueError:
                path_scope, runtime_path = "absolute_runtime", str(path)
            else:
                path_scope, runtime_path = "workspace_relative", relative.as_posix()
        else:
            path_scope, runtime_path = "repository_relative", relative.as_posix()
        materials.append(
            (
                {
                    "roles": sorted(metadata["roles"]),
                    "path_scope": path_scope,
                    "runtime_path": runtime_path,
                    "sha256": bytes_digest(data),
                    "size_bytes": len(data),
                },
                data,
            )
        )
    authority = {
        "schema_version": "1.0.0",
        "binding_kind": runtime_identity["kind"],
        "validator_id": binding.validator_id,
        "validator_version": binding.version,
        "runtime_identity": runtime_identity,
        "dependency_identities": dependency_identities,
        "dependency_policy": binding.dependency_policy,
        "files": [dict(metadata) for metadata, _ in materials],
        "coverage": {
            "bound": [
                "resolved executable and explicit command/module files"
                if binding.command
                else "callable code object, source file, and direct named dependency identities",
                (
                    "captured recursive repository-local Python, package-initializer, "
                    "JSON-Schema/$ref, semantic-root, registry, and runtime-pin closure"
                    if binding.dependency_policy == "derived_repository_closure_v2"
                    else "explicitly declared dependency files"
                ),
            ],
            "excluded": (
                [
                    "dynamic imports without a statically declared repository target",
                    "ambient process state",
                    "undeclared mutable external services",
                    "truth, proof, theorem, semantic-independence, and physics authority",
                ]
                if binding.dependency_policy == "derived_repository_closure_v2"
                else [
                    "undeclared transitive imports beyond explicit dependency paths",
                    "dynamic imports",
                    "ambient process state",
                    "undeclared mutable external services",
                ]
            ),
        },
    }
    return authority, effective_command, materials


def _validator_authority_digest(authority: Mapping[str, Any]) -> str:
    return canonical_digest({key: value for key, value in authority.items() if key != "authority_digest"})


def verify_current_validator_authority(
    authority: Mapping[str, Any],
    binding: ValidatorBinding,
    *,
    repository_root: Path = REPOSITORY_ROOT,
) -> None:
    """Re-hash the approved local validator closure against the current checkout.

    Historical receipts retain a sealed copy of every authority file. Exact
    release verification additionally resolves the production registry binding
    and re-hashes every repository-relative module/schema. Host executables are
    intentionally left as sealed historical runtime evidence so bundles remain
    portable across operating systems; local semantic Python and schema bytes
    must match the current checkout exactly.
    """

    if binding.dependency_policy not in {
        "derived_repository_closure_v2",
        "explicit_local_semantic_closure",
    }:
        raise ContractError(
            "current validator verification requires a closed local semantic policy"
        )
    if (
        authority.get("validator_id") != binding.validator_id
        or authority.get("validator_version") != binding.version
        or authority.get("dependency_policy") != binding.dependency_policy
    ):
        raise ContractError("validator authority does not match the approved registry binding")
    runtime = authority.get("runtime_identity", {})
    if runtime.get("kind") != "command" or runtime.get("declared_argv") != list(
        binding.command
    ):
        raise ContractError("validator authority command differs from the approved registry")
    expected_entry_module = (
        binding.command[2]
        if len(binding.command) >= 3 and binding.command[1] == "-m"
        else None
    )
    if not expected_entry_module or runtime.get("entry_module") != expected_entry_module:
        raise ContractError(
            "validator authority entry module differs from the approved registry"
        )

    expected_entry = expected_entry_module.replace(".", "/") + ".py"
    expected_roles: dict[str, set[str]] = {}
    expected_bytes: dict[str, bytes] = {}
    if binding.dependency_policy == "derived_repository_closure_v2":
        profile = binding.dependency_profile
        if profile is None or binding.registry_digest is None:
            raise ContractError("derived validator registry binding is incomplete")
        try:
            captured = capture_dependency_authority(
                **profile.authority_arguments(repository_root)
            )
        except DependencyAuthorityError as exc:
            raise ContractError(
                f"cannot derive current validator dependency closure: {exc}"
            ) from exc
        identities = [
            row
            for row in authority.get("dependency_identities", [])
            if isinstance(row, Mapping) and row.get("kind") == _DERIVED_CLOSURE_KIND
        ]
        if len(identities) != 1 or identities[0].get("authority") != captured.authority:
            raise ContractError(
                "validator derived repository closure differs from current registry/profile"
            )
        registry_bytes = captured.material_map().get(profile.registry_path)
        try:
            current_registry = (
                json.loads(registry_bytes.decode("utf-8"))
                if registry_bytes is not None
                else None
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ContractError("current validator registry is not canonical JSON") from exc
        if (
            not isinstance(current_registry, Mapping)
            or canonical_digest(current_registry) != binding.registry_digest
        ):
            raise ContractError("validator registry/current mismatch")
        expected_bytes = captured.material_map()
        expected_roles = {
            str(row["path"]): {"derived_dependency", *row["roles"]}
            for row in captured.authority["entries"]
        }
        if expected_entry not in expected_roles:
            raise ContractError("derived validator closure omits its entry module")
        expected_roles[expected_entry].add("entry_module")
        expected_paths = set(expected_roles)
    else:
        expected_paths = {
            safe_relative_path(path.removeprefix(_REPOSITORY_DEPENDENCY_PREFIX)).as_posix()
            for path in binding.dependency_paths
            if path.startswith(_REPOSITORY_DEPENDENCY_PREFIX)
        }
        if len(expected_paths) != len(binding.dependency_paths):
            raise ContractError(
                "explicit local semantic closure may contain only repository dependencies"
            )
        expected_paths.add(safe_relative_path(expected_entry).as_posix())

    local_rows: dict[str, Mapping[str, Any]] = {}
    for row in authority.get("files", []):
        if row.get("path_scope") != "repository_relative":
            continue
        runtime_path = safe_relative_path(str(row.get("runtime_path", ""))).as_posix()
        if runtime_path in local_rows:
            raise ContractError(f"validator authority repeats local path {runtime_path}")
        local_rows[runtime_path] = row
    if set(local_rows) != expected_paths:
        missing = sorted(expected_paths - set(local_rows))
        extra = sorted(set(local_rows) - expected_paths)
        raise ContractError(
            f"validator local semantic closure differs from registry; missing={missing}, extra={extra}"
        )
    for runtime_path, row in local_rows.items():
        if binding.dependency_policy == "derived_repository_closure_v2":
            if set(row.get("roles", [])) != expected_roles[runtime_path]:
                raise ContractError(
                    f"validator authority path {runtime_path} has substituted closure roles"
                )
            data = expected_bytes[runtime_path]
        else:
            expected_role = (
                "entry_module" if runtime_path == expected_entry else "declared_dependency"
            )
            if expected_role not in row.get("roles", []):
                raise ContractError(
                    f"validator authority path {runtime_path} lacks role {expected_role}"
                )
            source = repository_root.resolve() / safe_relative_path(runtime_path)
            if not source.is_file():
                raise ContractError(f"current validator dependency is missing: {runtime_path}")
            data = source.read_bytes()
        if bytes_digest(data) != row.get("sha256") or len(data) != row.get("size_bytes"):
            raise ContractError(
                f"current validator dependency differs from sealed authority: {runtime_path}"
            )


def validate_operator_request_identity(request: Mapping[str, Any]) -> None:
    """Recompute both full request identity and frozen-input identity."""

    validate_instance(request, "discovery_operator_request.schema.json")
    expected_request_digest = request_content_digest(request)
    if request.get("request_digest") != expected_request_digest:
        raise ContractError("operator request full-content digest mismatch")
    if request.get("request_id") != stable_identifier(
        "opreq", expected_request_digest
    ):
        raise ContractError("operator request ID is not content-derived")
    if request.get("input_digest") != _expected_input_digest(request):
        raise ContractError("operator request input_digest does not bind the declared inputs")


def _validator_receipt_digest(receipt: Mapping[str, Any]) -> str:
    return canonical_digest(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )


def validate_operator_receipt_identity(
    receipt: Mapping[str, Any], request: Mapping[str, Any] | None = None
) -> None:
    """Recompute the full receipt/validator identities and optional request binding."""

    validate_instance(receipt, "discovery_operator_receipt.schema.json")
    expected_receipt_digest = canonical_digest(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )
    if receipt.get("receipt_digest") != expected_receipt_digest:
        raise ContractError("operator receipt full-content digest mismatch")
    expected_receipt_id = stable_identifier(
        "opreceipt",
        receipt.get("request_id"),
        receipt.get("attempt"),
        canonical_digest(
            {
                key: value
                for key, value in receipt.items()
                if key not in {"receipt_id", "receipt_digest"}
            }
        ),
    )
    if receipt.get("receipt_id") != expected_receipt_id:
        raise ContractError("operator receipt ID is not content-derived")
    for validator in receipt.get("validator_receipts", []):
        if validator.get("receipt_digest") != _validator_receipt_digest(validator):
            raise ContractError("validator receipt full-content digest mismatch")
        authority = validator.get("validator_authority", {})
        if (
            authority.get("authority_digest") != _validator_authority_digest(authority)
            or validator.get("validator_code_digest") != authority.get("authority_digest")
            or authority.get("validator_id") != validator.get("validator_id")
            or authority.get("validator_version") != validator.get("validator_version")
        ):
            raise ContractError("validator receipt executable authority digest mismatch")
        if not validator_dependency_policy_is_supported(authority):
            raise ContractError("validator authority overclaims undeclared imports")
        if (
            validator.get("request_id") != receipt.get("request_id")
            or validator.get("input_digest") != receipt.get("input_digest")
            or validator.get("output_artifacts") != receipt.get("output_history_artifacts")
        ):
            raise ContractError("validator receipt does not bind exact request/input/history bytes")
    outputs = receipt.get("output_artifacts", [])
    history = receipt.get("output_history_artifacts", [])
    if len(outputs) != len(history):
        raise ContractError("operator receipt output/history cardinality mismatch")
    history_paths: set[str] = set()
    expected_prefix = (
        f".discovery-history/{receipt['identity']['target_id']}/{receipt['identity']['run_id']}/"
        f"{receipt['identity']['branch_id']}/state-{receipt['identity']['state_version']}/"
        f"{receipt['invocation_id']}/attempt-{receipt['attempt']}/outputs/"
    )
    for original, frozen in zip(outputs, history, strict=True):
        if (
            original.get("sha256") != frozen.get("sha256")
            or original.get("size_bytes") != frozen.get("size_bytes")
            or original.get("namespace") != frozen.get("namespace")
            or not str(frozen.get("path", "")).startswith(expected_prefix)
            or frozen.get("path") == original.get("path")
            or frozen.get("path") in history_paths
        ):
            raise ContractError("operator receipt lacks a unique immutable per-attempt output history")
        history_paths.add(str(frozen["path"]))
    if request is not None:
        validate_operator_request_identity(request)
        if (
            receipt.get("request_id") != request.get("request_id")
            or receipt.get("request_digest") != request.get("request_digest")
            or receipt.get("input_digest") != request.get("input_digest")
            or receipt.get("operator") != request.get("operator")
            or receipt.get("identity") != request.get("identity")
            or receipt.get("invocation_id") != request.get("invocation_id")
            or receipt.get("required") != request.get("required")
        ):
            raise ContractError("operator receipt does not bind the exact full request")


def build_operator_request(
    *,
    operator_id: str,
    operator_version: str,
    kind: str,
    namespace: Namespace,
    invocation_id: str,
    input_artifacts: Sequence[Mapping[str, Any]],
    declared_outputs: Sequence[str],
    parameters: Mapping[str, Any] | None = None,
    required: bool = True,
    requested_at: str | None = None,
) -> dict[str, Any]:
    """Construct and schema-validate a digest-bound operator request."""

    validate_identifier(invocation_id, "invocation_id")
    request = {
        "schema_version": "1.0.0",
        "invocation_id": invocation_id,
        "operator": {"operator_id": operator_id, "version": operator_version, "kind": kind},
        "identity": namespace.as_dict(),
        "required": required,
        "requested_at": requested_at or utc_now(),
        "parameters": dict(parameters or {}),
        "input_artifacts": [dict(item) for item in input_artifacts],
        "declared_outputs": [safe_relative_path(path).as_posix() for path in declared_outputs],
    }
    request["input_digest"] = _expected_input_digest(request)
    request["request_digest"] = request_content_digest(request)
    request["request_id"] = stable_identifier("opreq", request["request_digest"])
    validate_operator_request_identity(request)
    return request


def semantic_output_rows(
    operator_id: str, payload: Mapping[str, Any]
) -> list[dict[str, str]]:
    """Enumerate every decision-bearing output row that must reach an event.

    This is deliberately narrower than recursively treating every JSON scalar
    as a semantic assertion.  It closes the discovery protocol's explicit row
    classes: literature mappings, hypotheses, branch attempts, material
    reflection rounds, theory-programme consequences, and experiment
    assimilations.  Callers bind each returned row to one exact output path and
    one committed event.
    """

    rows: list[tuple[str, str, Any]] = []
    if operator_id == "frontier-literature-assimilator":
        rows.extend(
            ("assimilation_mapping", str(row["mapping_id"]), row)
            for row in payload.get("theory_mappings", [])
        )
    elif operator_id == "high-risk-hypothesis-forger":
        rows.extend(
            ("hypothesis", str(row["hypothesis_id"]), row)
            for row in payload.get("hypotheses", [])
        )
    elif operator_id == "parallel-hypothesis-portfolio":
        rows.extend(
            ("attempt", str(row["receipt_id"]), row)
            for row in payload.get("attempt_receipts", [])
        )
    elif operator_id in {
        "reflective-conceptual-discovery",
        "reflective-theory-synthesizer",
        "local-reflective-incubator",
        "local-reflective-synthesizer",
    }:
        packet_id = str(payload.get("packet_id", ""))
        for row in payload.get("reflection_rounds", []):
            mutation = row.get("mutation_or_synthesis", {})
            if (
                row.get("result") in {"mutated", "synthesized", "demoted"}
                and bool(mutation.get("changed_primitives_relations_or_explanation"))
            ):
                semantic_id = stable_identifier(
                    "semantic-reflection", packet_id, row.get("round_id"), canonical_digest(row)
                )
                rows.append(("material_reflection_round", semantic_id, row))
            elif row.get("result") == "no_change" and str(row.get("no_change_reason") or "").strip():
                # A documented failure to revise is feedback, but carries no
                # material-change claim. Keep it distinct in the semantic map.
                semantic_id = stable_identifier("reflection-plateau", payload["packet_id"], row["round_id"])
                rows.append(("reflection_plateau_round", semantic_id, row))
        programme = payload.get("theoretical_programme", {})
        programme_digest = canonical_digest(programme)
        for index, consequence in enumerate(programme.get("consequences_to_derive", [])):
            row = {
                "packet_id": packet_id,
                "packet_digest": payload.get("packet_digest"),
                "programme_id": programme.get("programme_id"),
                "programme_digest": programme_digest,
                "consequence_index": index,
                "consequence": consequence,
            }
            semantic_id = stable_identifier(
                "semantic-consequence", packet_id, index, consequence
            )
            rows.append(("synthesis_consequence", semantic_id, row))
    elif operator_id == "blind-conceptual-preference-adjudicator":
        evidence_id = str(payload.get("evidence_id", ""))
        preference_set = payload.get("preference_set", {})
        rows.append(("conceptual_adjudication_evidence", evidence_id, payload))
        rows.append(
            (
                "conceptual_preference_set",
                stable_identifier(
                    "conceptual-preference-set",
                    evidence_id,
                    preference_set.get("preference_set_digest"),
                ),
                preference_set,
            )
        )
    elif operator_id == "dynamic-symbolic-simulation-experimenter":
        rows.append(
            (
                "experiment_assimilation",
                str(payload.get("receipt_id")),
                {
                    "receipt_id": payload.get("receipt_id"),
                    "reflective_assimilation": payload.get("reflective_assimilation", []),
                },
            )
        )
    elif operator_id == "formal-claim-producer":
        material = {
            "output_id": payload.get("output_id"),
            "output_digest": payload.get("content_digest"),
            "status": payload.get("status"),
            "formal_claim_digest": payload.get("formal_claim_digest"),
            "source_semantic_row_id": payload.get("source_semantic_row_id"),
            "source_semantic_row_digest": payload.get(
                "source_semantic_row_digest"
            ),
        }
        rows.append(
            (
                "formal_claim_production",
                stable_identifier(
                    "semantic-formal-claim-production-v2", material
                ),
                material,
            )
        )
    return [
        {
            "semantic_kind": kind,
            "semantic_id": semantic_id,
            "row_digest": canonical_digest(row),
        }
        for kind, semantic_id, row in rows
    ]


class ReceiptStore:
    """Persist immutable per-attempt receipts in identity-local namespaces."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def path_for(self, receipt: Mapping[str, Any]) -> Path:
        """Return a safe path that cannot collide across branches or attempts."""

        namespace = Namespace.from_mapping(receipt["identity"])
        invocation = validate_identifier(receipt["invocation_id"], "invocation_id")
        attempt = receipt["attempt"]
        if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
            raise ContractError("receipt attempt must be a positive integer")
        return (
            self.root
            / namespace.target_id
            / namespace.run_id
            / namespace.branch_id
            / f"state-{namespace.state_version}"
            / invocation
            / f"attempt-{attempt}.json"
        )

    def write(self, receipt: Mapping[str, Any]) -> Path:
        """Atomically create an immutable receipt or accept an identical retry."""

        validate_operator_receipt_identity(receipt)
        path = self.path_for(receipt)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
        descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, path)
            except FileExistsError:
                if path.read_bytes() == data:
                    return path
                raise ContractError(f"receipt collision at {path}")
            fsync_directory(path.parent)
        finally:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
        return path


class DiscoveryOperatorDispatcher:
    """Run registered operators and produce an honest receipt for every attempt."""

    def __init__(
        self,
        bindings: Iterable[OperatorBinding],
        *,
        workspace: Path,
        receipt_store: ReceiptStore,
    ) -> None:
        self.workspace = workspace.resolve()
        self.receipt_store = receipt_store
        self.bindings: dict[str, OperatorBinding] = {}
        for binding in bindings:
            if binding.operator_id in self.bindings:
                raise ContractError(f"duplicate operator binding: {binding.operator_id}")
            self.bindings[binding.operator_id] = binding

    def _write_history_bytes(self, relative_path: str, data: bytes) -> Path:
        """Create one immutable workspace snapshot without an overwrite race."""

        path = resolve_workspace_path(self.workspace, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, path)
            except FileExistsError:
                if path.read_bytes() != data:
                    raise ContractError(f"immutable history collision at {path}")
            fsync_directory(path.parent)
        finally:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
        return path

    def _verify_request(self, request: Mapping[str, Any]) -> tuple[Namespace, OperatorBinding]:
        validate_operator_request_identity(request)
        namespace = Namespace.from_mapping(request["identity"])
        expected_digest = _expected_input_digest(request)
        if request["input_digest"] != expected_digest:
            raise ContractError("operator request input_digest does not bind the declared inputs")
        operator = request["operator"]
        binding = self.bindings.get(operator["operator_id"])
        if binding is None:
            raise ContractError(f"operator is not executable/registered: {operator['operator_id']}")
        if operator["version"] != binding.version or operator["kind"] != binding.kind:
            raise ContractError("operator request does not match the exact registered version and kind")
        input_paths: set[str] = set()
        for descriptor in request["input_artifacts"]:
            path_text = str(descriptor.get("path", ""))
            if path_text in input_paths:
                raise ContractError(f"operator request repeats input descriptor path: {path_text}")
            input_paths.add(path_text)
            _read_verified_descriptor(descriptor, self.workspace, namespace)
        for raw in request["declared_outputs"]:
            resolve_workspace_path(self.workspace, raw)
        return namespace, binding

    def _invoke_operator(
        self, binding: OperatorBinding, request: dict[str, Any]
    ) -> tuple[dict[str, Any], str, str, int | None]:
        if binding.function is not None:
            payload = binding.function(request, self.workspace)
            if not isinstance(payload, Mapping):
                raise ContractError("operator callable must return an object")
            return dict(payload), "", "", 0
        completed = subprocess.run(
            list(binding.command),
            cwd=self.workspace,
            input=canonical_json(request),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=binding.timeout_seconds,
            check=False,
        )
        stdout = completed.stdout.decode("utf-8", errors="replace")
        stderr = completed.stderr.decode("utf-8", errors="replace")
        if completed.returncode != 0:
            raise subprocess.CalledProcessError(
                completed.returncode, binding.command, output=completed.stdout, stderr=completed.stderr
            )
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise ContractError(f"operator stdout is not protocol JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise ContractError("operator stdout protocol must be an object")
        return payload, stdout, stderr, completed.returncode

    def _collect_outputs(
        self, request: Mapping[str, Any], protocol: Mapping[str, Any], namespace: Namespace
    ) -> tuple[list[dict[str, Any]], list[bytes]]:
        declared = set(request["declared_outputs"])
        reported = protocol.get("artifacts")
        if not isinstance(reported, list) or not reported:
            raise ContractError("successful operator returned no artifact paths")
        paths: list[str] = []
        for item in reported:
            raw = item.get("path") if isinstance(item, Mapping) else item
            if not isinstance(raw, str):
                raise ContractError("operator artifact report must contain paths")
            normalized = safe_relative_path(raw).as_posix()
            if normalized not in declared:
                raise ContractError(f"operator produced undeclared/unbound artifact: {normalized}")
            if normalized in paths:
                raise ContractError(f"operator reported duplicate artifact: {normalized}")
            paths.append(normalized)
        if set(paths) != declared:
            raise ContractError(f"operator did not produce every declared output: {sorted(declared - set(paths))}")
        descriptors: list[dict[str, Any]] = []
        materials: list[bytes] = []
        for path in sorted(paths):
            source = resolve_workspace_path(self.workspace, path, must_exist=True)
            data = source.read_bytes()
            descriptors.append(_descriptor_from_bytes(path, data, namespace))
            materials.append(data)
        return descriptors, materials

    def _freeze_outputs(
        self,
        request: Mapping[str, Any],
        attempt: int,
        namespace: Namespace,
        outputs: Sequence[Mapping[str, Any]],
        materials: Sequence[bytes],
    ) -> list[dict[str, Any]]:
        """Freeze every attempt output under a unique immutable history path."""

        base = (
            f".discovery-history/{namespace.target_id}/{namespace.run_id}/{namespace.branch_id}/"
            f"state-{namespace.state_version}/{request['invocation_id']}/attempt-{attempt}/outputs"
        )
        history: list[dict[str, Any]] = []
        for index, (output, data) in enumerate(zip(outputs, materials, strict=True)):
            suffix = Path(str(output["path"])).suffix or ".bin"
            name = stable_identifier(
                "output", request["request_id"], attempt, index, output["path"], output["sha256"]
            ) + suffix
            relative = f"{base}/{name}"
            self._write_history_bytes(relative, data)
            history.append(
                _descriptor_from_bytes(
                    relative,
                    data,
                    namespace,
                    media_type=output.get("media_type"),
                )
            )
        return history

    def _freeze_validator_authority(
        self,
        authority: Mapping[str, Any],
        materials: Sequence[tuple[dict[str, Any], bytes]],
        *,
        request: Mapping[str, Any],
        attempt: int,
        namespace: Namespace,
    ) -> dict[str, Any]:
        """Attach immutable snapshots to every explicitly bound validator file."""

        frozen = dict(authority)
        rows: list[dict[str, Any]] = []
        base = (
            f".discovery-history/{namespace.target_id}/{namespace.run_id}/{namespace.branch_id}/"
            f"state-{namespace.state_version}/{request['invocation_id']}/attempt-{attempt}/validators/"
            f"{authority['validator_id']}"
        )
        for index, (metadata, data) in enumerate(materials):
            suffix = Path(str(metadata["runtime_path"])).suffix or ".bin"
            name = stable_identifier(
                "authority", request["request_id"], attempt, authority["validator_id"], index, metadata["sha256"]
            ) + suffix
            relative = f"{base}/{name}"
            self._write_history_bytes(relative, data)
            row = dict(metadata)
            row["snapshot_descriptor"] = _descriptor_from_bytes(relative, data, namespace)
            rows.append(row)
        frozen["files"] = rows
        frozen["authority_digest"] = _validator_authority_digest(frozen)
        return frozen

    def _run_validator(
        self,
        binding: ValidatorBinding,
        request: dict[str, Any],
        execution_artifacts: list[dict[str, Any]],
        bound_artifacts: list[dict[str, Any]],
        *,
        attempt: int,
        namespace: Namespace,
    ) -> dict[str, Any]:
        started = utc_now()
        status, detail = "passed", None
        authority_core, effective_command, materials = _validator_authority_material(
            binding, self.workspace
        )
        authority = self._freeze_validator_authority(
            authority_core,
            materials,
            request=request,
            attempt=attempt,
            namespace=namespace,
        )
        try:
            if binding.function is not None:
                result = binding.function(request, execution_artifacts, self.workspace)
                if result is False:
                    raise ContractError("validator callable returned false")
            else:
                payload = canonical_json(
                    {"request": request, "artifacts": execution_artifacts}
                )
                completed = subprocess.run(
                    list(effective_command or ()),
                    cwd=self.workspace,
                    input=payload,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=binding.timeout_seconds,
                    check=False,
                )
                if completed.returncode != 0:
                    detail = completed.stderr.decode("utf-8", errors="replace")[-2000:]
                    raise ContractError(f"validator exited {completed.returncode}: {detail}")
            after_core, after_command, after_materials = _validator_authority_material(
                binding, self.workspace
            )
            if (
                after_command != effective_command
                or canonical_digest(after_core) != canonical_digest(authority_core)
                or [data for _, data in after_materials] != [data for _, data in materials]
            ):
                raise ContractError("validator executable authority changed during validation")
        except Exception as exc:
            status, detail = "failed", str(exc)
        receipt = {
            "validator_id": binding.validator_id,
            "validator_version": binding.version,
            "validator_code_digest": authority["authority_digest"],
            "validator_authority": authority,
            "request_id": request["request_id"],
            "input_digest": request["input_digest"],
            "started_at": started,
            "completed_at": utc_now(),
            "status": status,
            "artifact_digests": [artifact["sha256"] for artifact in bound_artifacts],
            "output_artifacts": [dict(artifact) for artifact in bound_artifacts],
        }
        if detail:
            receipt["detail"] = detail
        receipt["receipt_digest"] = _validator_receipt_digest(receipt)
        return receipt

    def dispatch(
        self,
        request: Mapping[str, Any],
        *,
        attempt: int = 1,
        skip_reason: str | None = None,
    ) -> dict[str, Any]:
        """Execute one attempt and persist a receipt even when execution fails."""

        started_at, monotonic_start = utc_now(), time.monotonic()
        namespace = Namespace.from_mapping(request.get("identity", {}))
        operator = dict(request.get("operator", {}))
        status = "failed"
        output_artifacts: list[dict[str, Any]] = []
        output_history_artifacts: list[dict[str, Any]] = []
        validator_receipts: list[dict[str, Any]] = []
        explicit_unknowns: list[str] = []
        search_provenance: dict[str, Any] | None = None
        stdout_digest = canonical_digest("")
        stderr_digest = canonical_digest("")
        exit_code: int | None = None
        error: dict[str, Any] | None = None
        try:
            verified_namespace, binding = self._verify_request(request)
            namespace.assert_matches(verified_namespace, context="request")
            if skip_reason is not None:
                if request["required"]:
                    raise DispatchBlocked("required operators cannot be skipped")
                if not skip_reason.strip():
                    raise ContractError("skip_reason must explain the justified skip")
                status = "skipped"
                explicit_unknowns = [skip_reason.strip()]
            else:
                protocol, stdout, stderr, exit_code = self._invoke_operator(binding, dict(request))
                stdout_digest, stderr_digest = canonical_digest(stdout), canonical_digest(stderr)
                output_artifacts, output_materials = self._collect_outputs(request, protocol, namespace)
                output_history_artifacts = self._freeze_outputs(
                    request,
                    attempt,
                    namespace,
                    output_artifacts,
                    output_materials,
                )
                raw_unknowns = protocol.get("explicit_unknowns", [])
                if not isinstance(raw_unknowns, list) or not all(
                    isinstance(item, str) and item.strip() for item in raw_unknowns
                ):
                    raise ContractError("explicit_unknowns must be a list of non-empty strings")
                explicit_unknowns = raw_unknowns
                if binding.kind == "literature_search":
                    raw_provenance = protocol.get("search_provenance")
                    if not isinstance(raw_provenance, Mapping):
                        raise ContractError("literature search omitted actual search_provenance")
                    search_provenance = dict(raw_provenance)
                validator_receipts = [
                    self._run_validator(
                        validator,
                        dict(request),
                        output_artifacts,
                        output_history_artifacts,
                        attempt=attempt,
                        namespace=namespace,
                    )
                    for validator in binding.validators
                ]
                for descriptor, frozen_bytes in zip(
                    output_artifacts, output_materials, strict=True
                ):
                    live = resolve_workspace_path(
                        self.workspace, descriptor["path"], must_exist=True
                    ).read_bytes()
                    if live != frozen_bytes:
                        raise DispatchBlocked(
                            "operator output changed while independent validation was running"
                        )
                if any(receipt["status"] != "passed" for receipt in validator_receipts):
                    raise DispatchBlocked("one or more independent validators failed")
                status = "succeeded"
        except subprocess.TimeoutExpired as exc:
            status = "timed_out"
            error = {"type": type(exc).__name__, "message": str(exc)}
        except subprocess.CalledProcessError as exc:
            status = "failed"
            exit_code = exc.returncode
            stdout_digest = canonical_digest((exc.stdout or b"").decode("utf-8", errors="replace"))
            stderr_digest = canonical_digest((exc.stderr or b"").decode("utf-8", errors="replace"))
            error = {"type": type(exc).__name__, "message": str(exc)}
            stderr_excerpt = _bounded_child_diagnostic(exc.stderr)
            if stderr_excerpt:
                error["stderr_excerpt"] = stderr_excerpt
        except Exception as exc:
            status = "failed"
            error = {
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback_digest": canonical_digest(traceback.format_exc()),
            }
        completed_at = utc_now()
        receipt: dict[str, Any] = {
            "schema_version": "1.0.0",
            "request_id": request.get("request_id"),
            "request_digest": request.get("request_digest"),
            "invocation_id": request.get("invocation_id"),
            "attempt": attempt,
            "operator": operator,
            "identity": namespace.as_dict(),
            "required": bool(request.get("required")),
            "input_digest": request.get("input_digest"),
            "started_at": started_at,
            "completed_at": completed_at,
            "duration_seconds": round(max(0.0, time.monotonic() - monotonic_start), 6),
            "status": status,
            "exit_code": exit_code,
            "stdout_digest": stdout_digest,
            "stderr_digest": stderr_digest,
            "output_artifacts": output_artifacts,
            "output_history_artifacts": output_history_artifacts,
            "explicit_unknowns": explicit_unknowns,
            "validator_receipts": validator_receipts,
        }
        if search_provenance is not None:
            receipt["search_provenance"] = search_provenance
        if error is not None:
            receipt["error"] = error
        receipt_content_digest = canonical_digest(receipt)
        receipt["receipt_id"] = stable_identifier(
            "opreceipt", request.get("request_id"), attempt, receipt_content_digest
        )
        receipt["receipt_digest"] = canonical_digest(receipt)
        # Receipt schema validation is intentionally last: malformed requests still
        # fail before persistence because they cannot truthfully name an invocation.
        self.receipt_store.write(receipt)
        return receipt

    def dispatch_many(self, requests: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
        """Run all requests without erasing valid siblings after one failure."""

        return [self.dispatch(request) for request in requests]


def ensure_evaluation_ready(
    requests: Sequence[Mapping[str, Any]],
    receipts: Sequence[Mapping[str, Any]],
    *,
    workspace: Path,
) -> None:
    """Block evaluation unless every required request has one valid success."""

    by_request: dict[str, list[Mapping[str, Any]]] = {}
    for receipt in receipts:
        validate_operator_receipt_identity(receipt)
        by_request.setdefault(receipt["request_id"], []).append(receipt)
    failures: list[str] = []
    for request in requests:
        validate_operator_request_identity(request)
        if not request["required"]:
            continue
        candidates = by_request.get(request["request_id"], [])
        successful = [receipt for receipt in candidates if receipt["status"] == "succeeded"]
        if not successful:
            failures.append(f"{request['request_id']}: no successful receipt")
            continue
        namespace = Namespace.from_mapping(request["identity"])
        receipt = max(successful, key=lambda item: item["attempt"])
        try:
            validate_operator_receipt_identity(receipt, request)
        except ContractError as exc:
            failures.append(f"{request['request_id']}: {exc}")
            continue
        if (
            receipt["input_digest"] != request["input_digest"]
            or receipt["operator"] != request["operator"]
            or receipt["identity"] != request["identity"]
        ):
            failures.append(f"{request['request_id']}: producer/consumer identity mismatch")
            continue
        try:
            for artifact in receipt["output_history_artifacts"]:
                _read_verified_descriptor(artifact, workspace, namespace)
            for validator in receipt["validator_receipts"]:
                for authority_file in validator["validator_authority"]["files"]:
                    _read_verified_descriptor(
                        authority_file["snapshot_descriptor"], workspace, namespace
                    )
            if not receipt["validator_receipts"] or any(
                validator["status"] != "passed" for validator in receipt["validator_receipts"]
            ):
                raise ContractError("missing successful validator evidence")
        except ContractError as exc:
            failures.append(f"{request['request_id']}: {exc}")
    if failures:
        raise DispatchBlocked("evaluation blocked: " + "; ".join(failures))


def assert_feedback_effective(
    receipts: Sequence[Mapping[str, Any]], feedback_edges: Sequence[Mapping[str, Any]]
) -> None:
    """Prove successful outputs were consumed by a durable state transition."""

    successful = {receipt["receipt_id"] for receipt in receipts if receipt.get("status") == "succeeded"}
    effective = {
        edge.get("producer_receipt_id")
        for edge in feedback_edges
        if edge.get("consumed") is True
        and edge.get("state_edge_committed") is True
        and isinstance(edge.get("consumer_event_id"), str)
    }
    missing = successful - effective
    if missing:
        raise DispatchBlocked(f"successful receipts lack feedback-effective consumption: {sorted(missing)}")
