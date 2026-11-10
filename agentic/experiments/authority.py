# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Observed transitive execution authority for dynamic experiments v3.

Dependency closure construction parses the complete local Python and schema
graph.  Repeating that reconstruction at every nested experiment validator is
both unnecessary and, for a five-world replay, approximately quadratic.  This
module therefore separates *derivation* from *reuse*:

* an explicit :class:`ExperimentAuthorityRunContext` derives the closure once,
  keeps only canonical immutable bytes, and performs one full dependency and
  environment replay when the operation exits; and
* standalone callers use a process-local memo only after byte-exact checks of
  every closed dependency, runtime-version checks, and import-resolution
  sentinels on every access.  A drifted sentinel forces a full reconstruction.

Neither route changes the authority boundary.  These records establish exact
local code, schema, environment, and executable identity only; they establish
no external truth, theorem, conceptual merit, or physics authority.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import stat
import sys
import threading
from contextlib import contextmanager
from contextvars import ContextVar
from importlib import metadata
from pathlib import Path, PurePosixPath
from typing import Any, Iterator, Mapping

from agentic.discovery.contracts import (
    ROOT,
    canonical_digest,
    canonical_json,
    file_digest,
)
from agentic.discovery.dependency_authority import (
    DependencyAuthorityError,
    build_dependency_authority,
)

from .errors import ExperimentAuthorityError


AUTHORITY_VERSION = "dynamic-experiment-authority/3.0.0"
AUTHORITY_SCOPE = "dynamic-experiment-runtime-v3"
AUTHORITY_BOUNDARY = (
    "exact_local_dependency_environment_and_executable_identity_only_"
    "not_external_truth_theorem_or_physics_authority"
)
_ENTRY_PATHS = {
    "agentic/experiments/runtime.py": ("runtime_dispatch_and_validation",),
    "agentic/experiments/adapters.py": ("adapter_implementation",),
}
_SEMANTIC_PATHS = {
    "agentic/spec/dynamic_experiment_spec_v2.schema.json": (
        "frozen_historical_v2_compatibility_contract",
    ),
    "agentic/spec/dynamic_experiment_receipt_v2.schema.json": (
        "frozen_historical_v2_compatibility_contract",
    ),
    "agentic/spec/dynamic_experiment_v3_common.schema.json": (
        "portable_v3_shared_type_contract",
    ),
    "agentic/spec/dynamic_experiment_spec_v3.schema.json": (
        "portable_v3_specification_contract",
    ),
    "agentic/spec/dynamic_experiment_receipt_v3.schema.json": (
        "portable_v3_execution_receipt_contract",
    ),
    "agentic/spec/dynamic_experiment_reflection_receipt_v1.schema.json": (
        "executed_post_result_reflection_contract",
    ),
}
_RUNTIME_DISTRIBUTIONS = {
    "jsonschema": "jsonschema",
    "referencing": "referencing",
}


_RUN_CONTEXT_CONSTRUCTION_KEY = object()
_DEPENDENCY_MEMO_LOCK = threading.RLock()
_DEPENDENCY_MEMO: _ExperimentDependencyAuthorityContext | None = None
_ACTIVE_RUN_CONTEXT: ContextVar[ExperimentAuthorityRunContext | None] = ContextVar(
    "dynamic_experiment_authority_run_context", default=None
)


class _DependencySnapshotDrift(RuntimeError):
    """Signal that a fast snapshot no longer names the current closure inputs."""


def _profile_digest() -> str:
    """Bind every static input that selects the experiment dependency graph."""

    return canonical_digest(
        {
            "repository_root": str(Path(ROOT).resolve()),
            "scope": AUTHORITY_SCOPE,
            "entry_python_paths": _ENTRY_PATHS,
            "semantic_paths": _SEMANTIC_PATHS,
            "runtime_distributions": _RUNTIME_DISTRIBUTIONS,
            "authority_boundary": AUTHORITY_BOUNDARY,
        }
    )


def _safe_relative_path(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if (
        not raw
        or "\\" in raw
        or path.is_absolute()
        or path.as_posix() != raw
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise _DependencySnapshotDrift(f"dependency path is unsafe: {raw!r}")
    return path


def _read_regular_file_identity(root: Path, relative: str) -> tuple[int, str]:
    """Hash one root-anchored regular file without following a symlink edge."""

    path = _safe_relative_path(relative)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    descriptors: list[int] = []
    try:
        descriptor = os.open(root, directory_flags | no_follow)
        descriptors.append(descriptor)
        for part in path.parts[:-1]:
            descriptor = os.open(
                part,
                directory_flags | no_follow,
                dir_fd=descriptor,
            )
            descriptors.append(descriptor)
        file_descriptor = os.open(
            path.parts[-1], os.O_RDONLY | no_follow, dir_fd=descriptors[-1]
        )
        descriptors.append(file_descriptor)
        before = os.fstat(file_descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise _DependencySnapshotDrift(
                f"dependency is not a regular file: {relative}"
            )
        digest = hashlib.sha256()
        while True:
            chunk = os.read(file_descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
        after = os.fstat(file_descriptor)
        identity_fields = (
            "st_dev",
            "st_ino",
            "st_mode",
            "st_size",
            "st_mtime_ns",
            "st_ctime_ns",
        )
        if any(getattr(before, field) != getattr(after, field) for field in identity_fields):
            raise _DependencySnapshotDrift(
                f"dependency changed while being hashed: {relative}"
            )
        current = os.stat(
            path.parts[-1], dir_fd=descriptors[-2], follow_symlinks=False
        )
        if current.st_dev != after.st_dev or current.st_ino != after.st_ino:
            raise _DependencySnapshotDrift(
                f"dependency path changed while being hashed: {relative}"
            )
        return int(after.st_size), f"sha256:{digest.hexdigest()}"
    except (FileNotFoundError, NotADirectoryError, OSError) as exc:
        if isinstance(exc, _DependencySnapshotDrift):
            raise
        raise _DependencySnapshotDrift(
            f"dependency cannot be reopened safely: {relative}"
        ) from exc
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _path_kind(root: Path, relative: str) -> str:
    """Return a no-follow path-shape sentinel for import resolution."""

    path = _safe_relative_path(relative)
    cursor = root
    try:
        for index, part in enumerate(path.parts):
            cursor = cursor / part
            value = cursor.lstat()
            if stat.S_ISLNK(value.st_mode):
                return "symlink"
            if index < len(path.parts) - 1 and not stat.S_ISDIR(value.st_mode):
                return "blocked"
    except FileNotFoundError:
        return "absent"
    mode = value.st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    return "special"


def _directory_inventory(
    root: Path, relative: str
) -> tuple[tuple[str, str], ...]:
    """Snapshot one directory's names and no-follow entry kinds.

    Watching the nearest existing parent of every absent module candidate is
    equivalent to probing hundreds of negative paths separately: creating any
    candidate must first change exactly one watched parent inventory.  The
    coarser inventory can trigger harmless extra rebuilds, but it cannot hide a
    resolution-changing file or package addition.
    """

    directory = root if relative == "." else root / _safe_relative_path(relative)
    if relative != "." and _path_kind(root, relative) != "directory":
        raise _DependencySnapshotDrift(
            f"import-sentinel directory changed: {relative}"
        )
    try:
        rows: list[tuple[str, str]] = []
        with os.scandir(directory) as entries:
            for entry in entries:
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISREG(mode):
                    kind = "regular"
                elif stat.S_ISDIR(mode):
                    kind = "directory"
                elif stat.S_ISLNK(mode):
                    kind = "symlink"
                else:
                    kind = "special"
                rows.append((entry.name, kind))
        return tuple(sorted(rows))
    except OSError as exc:
        raise _DependencySnapshotDrift(
            f"cannot inventory import-sentinel directory: {relative}"
        ) from exc


def _nearest_existing_parent(root: Path, relative: str) -> str:
    """Locate the directory whose inventory controls an absent candidate."""

    cursor = root
    for part in _safe_relative_path(relative).parts:
        candidate = cursor / part
        try:
            value = candidate.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(value.st_mode) or not stat.S_ISDIR(value.st_mode):
            break
        cursor = candidate
    return "." if cursor == root else cursor.relative_to(root).as_posix()


def _module_name(relative: str) -> str:
    path = PurePosixPath(relative)
    parts = list(path.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _relative_import_base(relative: str, node: ast.ImportFrom) -> str:
    module = _module_name(relative)
    package = module if relative.endswith("/__init__.py") else module.rpartition(".")[0]
    parts = package.split(".") if package else []
    keep = len(parts) - (node.level - 1)
    base = parts[:keep]
    if node.module:
        base.extend(node.module.split("."))
    return ".".join(base)


def _add_module_sentinels(
    sentinels: set[str], module: str, *, source: str | None
) -> None:
    """Watch every path whose appearance could change local import resolution."""

    if not module or any(
        not part or not part.isidentifier() for part in module.split(".")
    ):
        return
    sentinels.add(module.split(".", 1)[0])
    prefixes = [PurePosixPath()]
    if source is not None:
        source_parent = PurePosixPath(source).parent
        if source_parent not in prefixes:
            prefixes.append(source_parent)
    for prefix in prefixes:
        base = prefix.joinpath(*module.split("."))
        sentinels.add(f"{base.as_posix()}.py")
        sentinels.add(f"{base.as_posix()}/__init__.py")


def _import_resolution_sentinels(
    root: Path, authority: Mapping[str, Any]
) -> tuple[tuple[str, tuple[tuple[str, str], ...]], ...]:
    """Capture directory inventories controlling negative import resolution."""

    python_paths = authority["import_boundary"]["repository_local_python_paths"]
    sentinels: set[str] = set()
    for relative in python_paths:
        path = root / PurePosixPath(relative)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            raise _DependencySnapshotDrift(
                f"cannot derive import sentinels for {relative}: {exc}"
            ) from exc
        parent_parts = PurePosixPath(relative).parent.parts
        for length in range(1, len(parent_parts) + 1):
            sentinels.add(
                PurePosixPath(*parent_parts[:length], "__init__.py").as_posix()
            )
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    _add_module_sentinels(
                        sentinels, alias.name, source=str(relative)
                    )
            elif isinstance(node, ast.ImportFrom):
                base = (
                    _relative_import_base(str(relative), node)
                    if node.level
                    else str(node.module or "")
                )
                importing_source = None if node.level else str(relative)
                _add_module_sentinels(
                    sentinels, base, source=importing_source
                )
                for alias in node.names:
                    if alias.name != "*":
                        candidate = f"{base}.{alias.name}" if base else alias.name
                        _add_module_sentinels(
                            sentinels, candidate, source=importing_source
                        )
    watched_directories = {
        _nearest_existing_parent(root, relative)
        for relative in sentinels
        if _path_kind(root, relative) == "absent"
    }
    return tuple(
        (relative, _directory_inventory(root, relative))
        for relative in sorted(watched_directories)
    )


class _ExperimentDependencyAuthorityContext:
    """Immutable closure bytes plus exact cheap checks for every rebuild input."""

    __slots__ = (
        "_authority_bytes",
        "_entry_identities",
        "_profile_digest",
        "_repository_root",
        "_directory_sentinels",
    )

    def __init__(
        self,
        authority: Mapping[str, Any],
        *,
        _construction_key: object,
    ) -> None:
        if _construction_key is not _RUN_CONTEXT_CONSTRUCTION_KEY:
            raise ExperimentAuthorityError(
                "authority_context_construction_forbidden",
                "dependency authority contexts require an exact reconstruction boundary",
            )
        root = Path(ROOT).resolve(strict=True)
        self._authority_bytes = canonical_json(copy.deepcopy(dict(authority)))
        self._repository_root = root
        self._profile_digest = _profile_digest()
        self._entry_identities = tuple(
            (
                str(row["path"]),
                int(row["byte_size"]),
                str(row["content_digest"]),
            )
            for row in authority["entries"]
        )
        self._directory_sentinels = _import_resolution_sentinels(root, authority)

    def snapshot(self, *, check_current: bool) -> dict[str, Any]:
        """Return detached exact bytes, optionally proving all inputs unchanged."""

        if check_current:
            self._assert_current()
        return json.loads(self._authority_bytes)

    def _assert_current(self) -> None:
        if Path(ROOT).resolve(strict=True) != self._repository_root:
            raise _DependencySnapshotDrift("experiment repository root changed")
        if _profile_digest() != self._profile_digest:
            raise _DependencySnapshotDrift("experiment dependency profile changed")
        for relative, expected_size, expected_digest in self._entry_identities:
            size, digest = _read_regular_file_identity(
                self._repository_root, relative
            )
            if size != expected_size or digest != expected_digest:
                raise _DependencySnapshotDrift(
                    f"experiment dependency bytes changed: {relative}"
                )
        for relative, expected_inventory in self._directory_sentinels:
            if (
                _directory_inventory(self._repository_root, relative)
                != expected_inventory
            ):
                raise _DependencySnapshotDrift(
                    f"experiment import-resolution directory changed: {relative}"
                )
        authority = json.loads(self._authority_bytes)
        expected_runtime = [
            {"name": "python", "version": platform.python_version()},
            *[
                {"name": distribution, "version": metadata.version(distribution)}
                for distribution in sorted(set(_RUNTIME_DISTRIBUTIONS.values()))
            ],
        ]
        if authority["runtime_dependencies"] != expected_runtime:
            raise _DependencySnapshotDrift(
                "experiment runtime distribution versions changed"
            )


class ExperimentAuthorityRunContext:
    """Opaque operation-local authority reuse with one exact terminal replay.

    Construct contexts only through :func:`experiment_authority_run_context`.
    Warm validation returns defensive copies of canonical bytes; it never turns
    an authority digest or a caller mapping into cache authority.  The closing
    replay rebuilds the complete AST/schema closure and every environment used
    during the operation, so drift cannot silently survive the boundary.
    """

    __slots__ = (
        "_authorities",
        "_dependency_context",
        "_finalized",
        "_lock",
        "_replay_counts",
    )

    def __init__(
        self,
        dependency: Mapping[str, Any],
        *,
        _construction_key: object,
    ) -> None:
        if _construction_key is not _RUN_CONTEXT_CONSTRUCTION_KEY:
            raise ExperimentAuthorityError(
                "authority_context_construction_forbidden",
                "experiment authority run contexts require an exact boundary",
            )
        self._dependency_context = _ExperimentDependencyAuthorityContext(
            dependency, _construction_key=_RUN_CONTEXT_CONSTRUCTION_KEY
        )
        self._authorities: dict[bytes, bytes] = {}
        self._finalized = False
        self._lock = threading.RLock()
        self._replay_counts = {
            "dependency_full_replays": 1,
            "environment_observations": 0,
            "authority_cache_hits": 0,
            "final_dependency_replays": 0,
            "final_environment_replays": 0,
        }

    @property
    def replay_counts(self) -> dict[str, int]:
        """Return a detached audit of cold, warm, and terminal validation work."""

        with self._lock:
            return dict(self._replay_counts)

    def dependency_snapshot(self) -> dict[str, Any]:
        with self._lock:
            if self._finalized:
                raise ExperimentAuthorityError(
                    "authority_context_finalized",
                    "experiment authority run context is already finalized",
                )
            return self._dependency_context.snapshot(check_current=False)

    def build_authority(
        self, *, adapter: str, model: Mapping[str, Any]
    ) -> dict[str, Any]:
        with self._lock:
            if self._finalized:
                raise ExperimentAuthorityError(
                    "authority_context_finalized",
                    "experiment authority run context is already finalized",
                )
            key = canonical_json(
                {"adapter": adapter, "model": copy.deepcopy(dict(model))}
            )
            cached = self._authorities.get(key)
            if cached is not None:
                self._replay_counts["authority_cache_hits"] += 1
                return json.loads(cached)
            authority = _assemble_experiment_authority(
                dependency=self._dependency_context.snapshot(check_current=False),
                adapter=adapter,
                model=model,
            )
            encoded = canonical_json(authority)
            self._authorities[key] = encoded
            self._replay_counts["environment_observations"] += 1
            return json.loads(encoded)

    def assert_unchanged(self) -> None:
        """Rebuild the complete closure and every used environment exactly once."""

        with self._lock:
            if self._finalized:
                return
            try:
                initial_dependency = self._dependency_context.snapshot(
                    check_current=False
                )
                current_dependency = _build_experiment_dependency_authority_uncached()
                self._replay_counts["final_dependency_replays"] += 1
                if current_dependency != initial_dependency:
                    raise ExperimentAuthorityError(
                        "execution_authority_stale",
                        "experiment dependency authority drifted during the operation",
                    )
                for key, encoded in self._authorities.items():
                    request = json.loads(key)
                    current = _assemble_experiment_authority(
                        dependency=current_dependency,
                        adapter=str(request["adapter"]),
                        model=request["model"],
                    )
                    self._replay_counts["final_environment_replays"] += 1
                    if current != json.loads(encoded):
                        raise ExperimentAuthorityError(
                            "execution_authority_stale",
                            "experiment environment or executable authority drifted during the operation",
                        )
            finally:
                # A context that failed its closing replay is poisoned.  It
                # must never be retained by a caller and reused after drift.
                self._finalized = True


@contextmanager
def experiment_authority_run_context() -> Iterator[ExperimentAuthorityRunContext]:
    """Reuse exact authority within one operation and fully replay it on exit."""

    existing = _ACTIVE_RUN_CONTEXT.get()
    if existing is not None:
        yield existing
        return
    context = ExperimentAuthorityRunContext(
        _build_experiment_dependency_authority_uncached(),
        _construction_key=_RUN_CONTEXT_CONSTRUCTION_KEY,
    )
    token = _ACTIVE_RUN_CONTEXT.set(context)
    try:
        yield context
    finally:
        try:
            context.assert_unchanged()
        finally:
            _ACTIVE_RUN_CONTEXT.reset(token)


def _top_level_digest(value: Mapping[str, Any], digest_field: str) -> str:
    """Hash exact nested semantics while omitting only one root self-field."""

    material = dict(value)
    material.pop(digest_field, None)
    return canonical_digest(material)


def _regular_executable(path: Path, *, label: str) -> dict[str, Any]:
    """Record the resolved bytes of one executable and fail closed otherwise."""

    try:
        resolved = path.resolve(strict=True)
        file_stat = resolved.stat()
    except OSError as exc:
        raise ExperimentAuthorityError(
            "executable_unavailable",
            f"{label} executable cannot be resolved: {path}",
        ) from exc
    if not stat.S_ISREG(file_stat.st_mode) or not os.access(resolved, os.X_OK):
        raise ExperimentAuthorityError(
            "executable_not_regular",
            f"{label} executable is not an executable regular file: {resolved}",
        )
    return {
        "resolved_path": str(resolved),
        "byte_size": file_stat.st_size,
        "content_digest": file_digest(resolved),
    }


def _build_experiment_dependency_authority_uncached() -> dict[str, Any]:
    """Perform one complete AST/import/schema/runtime authority derivation."""

    try:
        return build_dependency_authority(
            scope=AUTHORITY_SCOPE,
            entry_python_paths=_ENTRY_PATHS,
            semantic_paths=_SEMANTIC_PATHS,
            authority_boundary=AUTHORITY_BOUNDARY,
            repository_root=ROOT,
            runtime_distributions=_RUNTIME_DISTRIBUTIONS,
        )
    except DependencyAuthorityError as exc:
        raise ExperimentAuthorityError(
            "dependency_authority_invalid",
            str(exc),
        ) from exc


def _memoized_experiment_dependency_authority() -> dict[str, Any]:
    """Reuse a closure only while every exact rebuild input remains unchanged.

    The memo is not an authority source.  Its warm path rehashes all closed
    files, checks installed runtime versions, and checks both positive and
    negative module-resolution paths.  Any discrepancy discards the memo and
    runs the complete closure builder before returning or failing.
    """

    global _DEPENDENCY_MEMO
    with _DEPENDENCY_MEMO_LOCK:
        if _DEPENDENCY_MEMO is not None:
            try:
                return _DEPENDENCY_MEMO.snapshot(check_current=True)
            except (
                _DependencySnapshotDrift,
                metadata.PackageNotFoundError,
                OSError,
            ):
                _DEPENDENCY_MEMO = None
        authority = _build_experiment_dependency_authority_uncached()
        try:
            context = _ExperimentDependencyAuthorityContext(
                authority, _construction_key=_RUN_CONTEXT_CONSTRUCTION_KEY
            )
            # Close construction-time races before publishing the memo.
            snapshot = context.snapshot(check_current=True)
        except (
            _DependencySnapshotDrift,
            metadata.PackageNotFoundError,
            OSError,
        ) as exc:
            raise ExperimentAuthorityError(
                "dependency_authority_invalid",
                f"dependency authority changed during reconstruction: {exc}",
            ) from exc
        _DEPENDENCY_MEMO = context
        return snapshot


def _reset_experiment_authority_memo_for_tests() -> None:
    """Clear process-local acceleration state for isolated regression tests."""

    global _DEPENDENCY_MEMO
    with _DEPENDENCY_MEMO_LOCK:
        _DEPENDENCY_MEMO = None


def build_experiment_dependency_authority() -> dict[str, Any]:
    """Return current exact dependency authority with drift-checked reuse."""

    context = _ACTIVE_RUN_CONTEXT.get()
    if context is not None:
        return context.dependency_snapshot()
    return _memoized_experiment_dependency_authority()


def _distribution_capability(module: str, distribution: str) -> dict[str, Any]:
    available = importlib.util.find_spec(module) is not None
    if not available:
        return {"available": False, "distribution": distribution, "version": None}
    try:
        version = metadata.version(distribution)
    except metadata.PackageNotFoundError as exc:
        raise ExperimentAuthorityError(
            "capability_distribution_unpinned",
            f"available module {module!r} lacks distribution metadata",
        ) from exc
    return {"available": True, "distribution": distribution, "version": version}


def _lean_requests(adapter: str, model: Mapping[str, Any]) -> list[dict[str, Any]]:
    requested: list[tuple[str, str]] = []
    if adapter == "lean":
        requested.append(("root", str(model.get("executable", "lean"))))
    elif adapter == "hybrid":
        stages = model.get("stages", [])
        if isinstance(stages, list):
            for index, stage in enumerate(stages):
                if not isinstance(stage, Mapping) or stage.get("adapter") != "lean":
                    continue
                stage_model = stage.get("model", {})
                if not isinstance(stage_model, Mapping):
                    stage_model = {}
                requested.append(
                    (
                        f"stage-{index:02d}",
                        str(stage_model.get("executable", "lean")),
                    )
                )
    records: list[dict[str, Any]] = []
    for stage, command in requested:
        resolved = shutil.which(command)
        records.append(
            {
                "stage": stage,
                "requested": command,
                "available": resolved is not None,
                "executable": (
                    _regular_executable(Path(resolved), label=f"Lean {stage}")
                    if resolved is not None
                    else None
                ),
            }
        )
    return records


def build_observed_environment(
    *, adapter: str, model: Mapping[str, Any]
) -> dict[str, Any]:
    """Observe rather than accept the runtime environment and solver bytes."""

    python_executable = _regular_executable(Path(sys.executable), label="Python")
    lean_requests = _lean_requests(adapter, model)
    lean_capability: dict[str, Any] = {
        "requests": lean_requests,
        "all_available": bool(lean_requests)
        and all(row["available"] for row in lean_requests),
        "any_available": any(row["available"] for row in lean_requests),
    }
    environment: dict[str, Any] = {
        "environment_version": "dynamic-experiment-observed-environment/3.0.0",
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "cache_tag": sys.implementation.cache_tag,
            "executable": python_executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "capabilities": {
            "sympy": _distribution_capability("sympy", "sympy"),
            "lean": lean_capability,
        },
    }
    environment["content_digest"] = _top_level_digest(
        environment, "content_digest"
    )
    return environment


def build_experiment_authority(
    *, adapter: str, model: Mapping[str, Any]
) -> dict[str, Any]:
    """Bind transitive code, observed process environment, and executables."""

    context = _ACTIVE_RUN_CONTEXT.get()
    if context is not None:
        return context.build_authority(adapter=adapter, model=model)
    return _assemble_experiment_authority(
        dependency=build_experiment_dependency_authority(),
        adapter=adapter,
        model=model,
    )


def _assemble_experiment_authority(
    *,
    dependency: Mapping[str, Any],
    adapter: str,
    model: Mapping[str, Any],
) -> dict[str, Any]:
    """Combine one already-derived closure with a fresh observed environment."""

    environment = build_observed_environment(adapter=adapter, model=model)
    authority: dict[str, Any] = {
        "authority_version": AUTHORITY_VERSION,
        "dependency_authority": copy.deepcopy(dict(dependency)),
        "observed_environment": environment,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    authority["content_digest"] = _top_level_digest(authority, "content_digest")
    return authority


def validate_experiment_authority(
    record: Mapping[str, Any], *, adapter: str, model: Mapping[str, Any]
) -> dict[str, Any]:
    """Rebuild current authority and reject any byte/environment relabelling."""

    if not isinstance(record, Mapping):
        raise ExperimentAuthorityError(
            "authority_not_object", "execution authority must be an object"
        )
    supplied = dict(record)
    if supplied.get("content_digest") != _top_level_digest(
        supplied, "content_digest"
    ):
        raise ExperimentAuthorityError(
            "authority_self_digest_mismatch",
            "execution authority top-level content digest is invalid",
        )
    expected = build_experiment_authority(adapter=adapter, model=model)
    if supplied != expected:
        raise ExperimentAuthorityError(
            "execution_authority_stale",
            "dependency, environment, or executable authority differs from current observation",
        )
    return expected


__all__ = [
    "AUTHORITY_BOUNDARY",
    "AUTHORITY_SCOPE",
    "AUTHORITY_VERSION",
    "ExperimentAuthorityRunContext",
    "build_experiment_authority",
    "build_experiment_dependency_authority",
    "build_observed_environment",
    "experiment_authority_run_context",
    "validate_experiment_authority",
]
