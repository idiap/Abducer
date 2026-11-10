# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Build exact, reusable authority over a bounded local dependency graph.

An authority record is meaningful only if its file set is derived rather than
remembered by a caller. This module starts from named Python entry points,
walks every statically imported repository-local module (including package
initializers), discovers JSON-Schema path literals in the resulting syntax
trees, seeds every explicitly declared semantic JSON-Schema root, follows
local ``$ref`` edges from both root classes, and then hashes the complete
closed set.

The result proves byte identity and graph completeness for this finite local
profile. It does not prove that the code is correct, that a schema is
scientifically adequate, or that an external package is trustworthy. Dynamic
imports whose module targets are not represented by ordinary AST import
statements must be promoted to named Python entry points; non-code semantic
extras belong in semantic paths. Unclassified third-party imports fail closed.
"""

from __future__ import annotations

import ast
import dataclasses
import errno
import json
import os
import platform
import re
import stat
import sys
from importlib import metadata
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

from .contracts import (
    ROOT,
    LocalSchemaResolutionError,
    bytes_digest,
    canonical_digest,
    resolve_local_schema_reference,
    schema_document_references,
    schema_resource_ids,
)


AUTHORITY_VERSION = "2.0.0"
IMPORT_POLICY = "conservative_repository_local_ast_import_closure_v2"
_SCHEMA_LITERAL = re.compile(
    r"^(?:agentic/spec/)?(?:[A-Za-z0-9_.-]+/)*"
    r"[A-Za-z0-9][A-Za-z0-9_.-]*\.schema\.json$"
)


class DependencyAuthorityError(ValueError):
    """Raised when a dependency profile is incomplete, unsafe, or stale."""


@dataclasses.dataclass(frozen=True, slots=True)
class CapturedDependencyAuthority:
    """One authority and the exact immutable bytes from which it was derived."""

    authority: dict[str, Any]
    materials: tuple[tuple[str, bytes], ...]

    def material_map(self) -> dict[str, bytes]:
        """Return a detached path-to-bytes projection for snapshot persistence."""

        return dict(self.materials)


@dataclasses.dataclass(frozen=True, slots=True)
class _CapturedPathIdentity:
    """Identity of every opened parent plus the final regular file."""

    parent_directories: tuple[tuple[int, int, int], ...]
    regular_file: tuple[int, int, int, int, int, int]


def _stat_identity(value: os.stat_result) -> tuple[int, int, int, int, int, int]:
    """Return the file identity and mutation fields relevant to one capture."""

    return (
        value.st_dev,
        value.st_ino,
        stat.S_IFMT(value.st_mode),
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _directory_identity(value: os.stat_result) -> tuple[int, int, int]:
    """Return stable identity fields for one traversed directory."""

    return (value.st_dev, value.st_ino, stat.S_IFMT(value.st_mode))


def _open_regular_file_from_root(
    root: Path, relative: str
) -> tuple[int, _CapturedPathIdentity]:
    """Open one file by component from a retained repository-root descriptor.

    A final-component ``O_NOFOLLOW`` is insufficient: an attacker can replace
    an ancestor after a path-based safety check and before the final open.  This
    traversal retains each parent descriptor, opens the next component with
    ``openat``/``O_NOFOLLOW``, and records every parent identity for the later
    named-path stability check.
    """

    normalized = _relative_path(relative)
    if (
        not hasattr(os, "O_NOFOLLOW")
        or not hasattr(os, "O_DIRECTORY")
    ):
        raise DependencyAuthorityError(
            "component-wise no-follow dependency traversal is unavailable"
        )
    directory_flags = (
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    )
    file_flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    parent_descriptors: list[int] = []
    file_descriptor: int | None = None
    try:
        named_root_before = os.stat(root, follow_symlinks=False)
        root_descriptor = os.open(root, directory_flags)
        parent_descriptors.append(root_descriptor)
        root_opened = os.fstat(root_descriptor)
        if (
            not stat.S_ISDIR(root_opened.st_mode)
            or _directory_identity(named_root_before)
            != _directory_identity(root_opened)
        ):
            raise DependencyAuthorityError(
                "repository root changed while opening dependency authority"
            )

        parent_identities = [_directory_identity(root_opened)]
        cursor_descriptor = root_descriptor
        parts = PurePosixPath(normalized).parts
        for component in parts[:-1]:
            next_descriptor = os.open(
                component,
                directory_flags,
                dir_fd=cursor_descriptor,
            )
            parent_descriptors.append(next_descriptor)
            opened_parent = os.fstat(next_descriptor)
            if not stat.S_ISDIR(opened_parent.st_mode):
                raise DependencyAuthorityError(
                    f"dependency parent is not a directory: {normalized}"
                )
            parent_identities.append(_directory_identity(opened_parent))
            cursor_descriptor = next_descriptor

        file_descriptor = os.open(
            parts[-1],
            file_flags,
            dir_fd=cursor_descriptor,
        )
        opened_file = os.fstat(file_descriptor)
        if not stat.S_ISREG(opened_file.st_mode):
            raise DependencyAuthorityError(
                f"dependency must be a regular file: {normalized}"
            )
        named_root_after = os.stat(root, follow_symlinks=False)
        if (
            _directory_identity(named_root_after)
            != _directory_identity(root_opened)
        ):
            raise DependencyAuthorityError(
                "repository root changed while traversing dependency authority"
            )
        result = file_descriptor
        file_descriptor = None
        return result, _CapturedPathIdentity(
            parent_directories=tuple(parent_identities),
            regular_file=_stat_identity(opened_file),
        )
    except DependencyAuthorityError:
        raise
    except (OSError, TypeError) as exc:
        if isinstance(exc, OSError) and exc.errno == errno.ELOOP:
            raise DependencyAuthorityError(
                f"dependency path traverses a symlink: {normalized}"
            ) from exc
        raise DependencyAuthorityError(
            f"cannot traverse repository dependency {normalized}: {exc}"
        ) from exc
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        for descriptor in reversed(parent_descriptors):
            os.close(descriptor)


def _capture_regular_file(
    root: Path, relative: str
) -> tuple[bytes, _CapturedPathIdentity]:
    """Read one component-wise no-follow file and retain its full path identity."""

    descriptor, identity = _open_regular_file_from_root(root, relative)
    try:
        opened = os.fstat(descriptor)
        if _stat_identity(opened) != identity.regular_file:
            raise DependencyAuthorityError(
                f"dependency changed while opening: {relative}"
            )
        chunks: list[bytes] = []
        while chunk := os.read(descriptor, 1024 * 1024):
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if _stat_identity(opened) != _stat_identity(after):
            raise DependencyAuthorityError(
                f"dependency changed while reading: {relative}"
            )
        data = b"".join(chunks)
        if len(data) != after.st_size:
            raise DependencyAuthorityError(
                f"dependency size changed while reading: {relative}"
            )
        return data, identity
    finally:
        os.close(descriptor)


class _RepositoryByteCapture:
    """Cache exact repository bytes and prove their named files stayed stable."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self._captured: dict[str, tuple[bytes, _CapturedPathIdentity]] = {}

    def read(self, relative: str) -> bytes:
        captured = self._captured.get(relative)
        if captured is None:
            captured = _capture_regular_file(self.root, relative)
            self._captured[relative] = captured
        else:
            self._assert_one_stable(relative, captured[1])
        return captured[0]

    def _assert_one_stable(
        self, relative: str, identity: _CapturedPathIdentity
    ) -> None:
        try:
            descriptor, current = _open_regular_file_from_root(self.root, relative)
        except DependencyAuthorityError as exc:
            raise DependencyAuthorityError(
                f"dependency changed after capture: {relative}"
            ) from exc
        else:
            os.close(descriptor)
        if current != identity:
            raise DependencyAuthorityError(
                f"dependency changed after capture: {relative}"
            )

    def assert_stable(self) -> None:
        for relative, (_data, identity) in sorted(self._captured.items()):
            self._assert_one_stable(relative, identity)


def _relative_path(raw: str) -> str:
    """Return one canonical POSIX repository-relative path or fail closed."""

    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise DependencyAuthorityError(f"dependency path is not canonical: {raw!r}")
    path = PurePosixPath(raw)
    if (
        path.is_absolute()
        or path.as_posix() != raw
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise DependencyAuthorityError(f"dependency path is not safe: {raw!r}")
    return raw


def _repository_root(raw: Path | str) -> Path:
    path = Path(raw)
    if path.is_symlink() or not path.is_dir():
        raise DependencyAuthorityError("repository root must be a non-symlink directory")
    return path.resolve(strict=True)


def _safe_file(root: Path, relative: str) -> Path:
    """Resolve a regular file while rejecting every in-repository symlink edge."""

    normalized = _relative_path(relative)
    parts = PurePosixPath(normalized).parts
    cursor = root
    for index, part in enumerate(parts):
        cursor = cursor / part
        if cursor.is_symlink():
            raise DependencyAuthorityError(
                f"dependency path traverses a symlink: {normalized}"
            )
        if not cursor.exists():
            raise DependencyAuthorityError(f"dependency file is missing: {normalized}")
        if index < len(parts) - 1 and not cursor.is_dir():
            raise DependencyAuthorityError(
                f"dependency parent is not a directory: {normalized}"
            )
    resolved = cursor.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise DependencyAuthorityError(
            f"dependency escapes the repository root: {normalized}"
        ) from exc
    if not stat.S_ISREG(resolved.stat().st_mode):
        raise DependencyAuthorityError(
            f"dependency must be a regular file: {normalized}"
        )
    return resolved


def _roles(raw: Sequence[str], *, path: str) -> tuple[str, ...]:
    values = tuple(sorted(set(raw)))
    if not values or any(not isinstance(value, str) or not value.strip() for value in values):
        raise DependencyAuthorityError(f"dependency roles are invalid for {path}")
    return values


def _profile_paths(
    raw: Mapping[str, Sequence[str]], *, label: str
) -> dict[str, tuple[str, ...]]:
    if not isinstance(raw, Mapping) or not raw:
        raise DependencyAuthorityError(f"{label} must be a non-empty path-to-roles mapping")
    return {
        _relative_path(path): _roles(roles, path=path)
        for path, roles in sorted(raw.items())
    }


def _module_name(relative: str) -> str:
    path = PurePosixPath(relative)
    parts = list(path.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _module_path(root: Path, module: str, *, source: str | None = None) -> str | None:
    """Resolve a module against the repository and an importing script directory.

    Repository scripts intentionally place their own directory on ``sys.path``
    and use imports such as ``from agentic_common import ROOT``. Treating those
    imports as ambient packages would leave executable local code outside the
    authority. Both possible local resolutions are therefore considered, and
    any shadowing ambiguity fails closed instead of depending on launch mode.
    """

    if not module or any(not part or not part.isidentifier() for part in module.split(".")):
        return None
    prefixes = [PurePosixPath()]
    if source is not None:
        source_parent = PurePosixPath(_relative_path(source)).parent
        if source_parent not in prefixes:
            prefixes.append(source_parent)
    existing: set[str] = set()
    for prefix in prefixes:
        base = prefix.joinpath(*module.split("."))
        candidates = (f"{base.as_posix()}.py", f"{base.as_posix()}/__init__.py")
        for relative in candidates:
            absolute = root / PurePosixPath(relative)
            if absolute.exists() or absolute.is_symlink():
                _safe_file(root, relative)
                existing.add(relative)
    if len(existing) > 1:
        raise DependencyAuthorityError(
            f"ambiguous repository-local module: {module} -> {sorted(existing)}"
        )
    if not existing:
        return None
    return next(iter(existing))


def _package_initializers(root: Path, relative: str) -> list[str]:
    """Include package initializers because Python executes them before modules."""

    path = PurePosixPath(relative)
    directory_parts = list(path.parent.parts)
    result: list[str] = []
    for length in range(1, len(directory_parts) + 1):
        candidate = PurePosixPath(*directory_parts[:length], "__init__.py").as_posix()
        absolute = root / PurePosixPath(candidate)
        if absolute.exists() or absolute.is_symlink():
            _safe_file(root, candidate)
            result.append(candidate)
    if relative.endswith("/__init__.py") and relative in result:
        result.remove(relative)
    return result


def _relative_import_base(relative: str, node: ast.ImportFrom) -> str:
    module = _module_name(relative)
    package = module if relative.endswith("/__init__.py") else module.rpartition(".")[0]
    parts = package.split(".") if package else []
    if node.level > len(parts) + 1:
        raise DependencyAuthorityError(
            f"relative import escapes repository package in {relative}:{node.lineno}"
        )
    keep = len(parts) - (node.level - 1)
    base = parts[:keep]
    if node.module:
        base.extend(node.module.split("."))
    return ".".join(base)


def _schema_literals(tree: ast.AST) -> set[str]:
    return {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and _SCHEMA_LITERAL.fullmatch(node.value)
    }


def _schema_literal_path(literal: str) -> str:
    return literal if literal.startswith("agentic/spec/") else f"agentic/spec/{literal}"


def _schema_reference_path(root: Path, source: str, reference: str) -> str | None:
    """Resolve one local schema-document reference within the repository.

    Fragment-only references stay within the already hashed document.  Every
    URI scheme and network-path reference is outside this finite authority and
    therefore fails explicitly; it is never fetched or silently ignored.
    """

    try:
        candidate = resolve_local_schema_reference(
            reference,
            source_path=_safe_file(root, source),
            boundary_root=root,
            schema_root=root / "agentic/spec",
        )
    except LocalSchemaResolutionError as exc:
        if exc.reason_code == "path_escape":
            message = "schema reference escapes repository"
        elif exc.reason_code == "missing":
            message = "schema reference target is missing"
        else:
            message = "schema reference leaves bounded local authority"
        raise DependencyAuthorityError(
            f"{message}: {source} -> {reference} ({exc})"
        ) from exc
    if candidate is None:
        return None
    return candidate.relative_to(root).as_posix()


def _runtime_version(distribution: str) -> str:
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError as exc:
        raise DependencyAuthorityError(
            f"required runtime distribution is unavailable: {distribution}"
        ) from exc


def capture_dependency_authority(
    *,
    scope: str,
    entry_python_paths: Mapping[str, Sequence[str]],
    semantic_paths: Mapping[str, Sequence[str]],
    authority_boundary: str,
    repository_root: Path | str = ROOT,
    runtime_distributions: Mapping[str, str] | None = None,
) -> CapturedDependencyAuthority:
    """Capture, derive, and hash one local import/schema/semantic closure.

    ``runtime_distributions`` maps an imported top-level module to the installed
    distribution whose version pins that import (for example
    ``{"jsonschema": "jsonschema"}``). Every non-stdlib, non-local import must
    occur in that mapping, and unused mappings are rejected so the profile is an
    exact boundary rather than a grab bag of ambient packages.
    """

    if not isinstance(scope, str) or not scope.strip():
        raise DependencyAuthorityError("dependency authority scope is required")
    if not isinstance(authority_boundary, str) or len(authority_boundary.strip()) < 8:
        raise DependencyAuthorityError("dependency authority boundary is not substantive")
    root = _repository_root(repository_root)
    capture = _RepositoryByteCapture(root)
    entries = _profile_paths(entry_python_paths, label="entry_python_paths")
    semantics = _profile_paths(semantic_paths, label="semantic_paths")
    distributions = {
        str(module): str(distribution)
        for module, distribution in sorted((runtime_distributions or {}).items())
    }
    if any(
        not module.isidentifier() or not distribution.strip()
        for module, distribution in distributions.items()
    ):
        raise DependencyAuthorityError("runtime distribution mapping is invalid")

    path_roles: dict[str, set[str]] = {}
    python_paths: set[str] = set()
    trees: dict[str, ast.AST] = {}
    queue: list[str] = []
    stdlib_modules: set[str] = set()
    third_party_modules: set[str] = set()

    def add_path(relative: str, roles: Sequence[str]) -> None:
        capture.read(relative)
        path_roles.setdefault(relative, set()).update(roles)

    def add_python(relative: str, roles: Sequence[str]) -> None:
        add_path(relative, roles)
        if relative not in python_paths:
            python_paths.add(relative)
            queue.append(relative)
        for initializer in _package_initializers(root, relative):
            add_path(initializer, ("package_initializer", "repository_local_import"))
            if initializer not in python_paths:
                python_paths.add(initializer)
                queue.append(initializer)

    for relative, roles in entries.items():
        if not relative.endswith(".py"):
            raise DependencyAuthorityError(
                f"entry Python dependency does not end in .py: {relative}"
            )
        add_python(relative, (*roles, "entry_python"))
    for relative, roles in semantics.items():
        add_path(relative, (*roles, "semantic_extra"))

    def classify_external(module: str, *, source: str, required_local: bool) -> None:
        top_level = module.split(".", 1)[0]
        local_top = root / top_level
        if required_local or local_top.exists() or local_top.is_symlink():
            raise DependencyAuthorityError(
                f"repository-local import cannot be resolved: {module} from {source}"
            )
        if top_level in sys.stdlib_module_names or top_level == "__future__":
            stdlib_modules.add(module)
            return
        if top_level not in distributions:
            raise DependencyAuthorityError(
                f"third-party import lacks a runtime pin: {module} from {source}"
            )
        third_party_modules.add(top_level)

    while queue:
        relative = queue.pop()
        try:
            source = capture.read(relative).decode("utf-8")
            tree = ast.parse(source, filename=relative)
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            raise DependencyAuthorityError(
                f"cannot parse repository-local dependency {relative}: {exc}"
            ) from exc
        trees[relative] = tree
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported = _module_path(root, alias.name, source=relative)
                    if imported is None:
                        classify_external(alias.name, source=relative, required_local=False)
                    else:
                        add_python(imported, ("repository_local_import",))
            elif isinstance(node, ast.ImportFrom):
                base = (
                    _relative_import_base(relative, node)
                    if node.level
                    else str(node.module or "")
                )
                importing_source = None if node.level else relative
                imported_base = (
                    _module_path(root, base, source=importing_source) if base else None
                )
                imported_aliases = []
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    candidate = f"{base}.{alias.name}" if base else alias.name
                    imported_alias = _module_path(
                        root, candidate, source=importing_source
                    )
                    if imported_alias is not None:
                        imported_aliases.append(imported_alias)
                if imported_base is not None:
                    add_python(imported_base, ("repository_local_import",))
                elif not imported_aliases:
                    classify_external(
                        base,
                        source=relative,
                        required_local=bool(node.level),
                    )
                for imported_alias in imported_aliases:
                    add_python(imported_alias, ("repository_local_import",))

    unused_pins = set(distributions) - third_party_modules
    if unused_pins:
        raise DependencyAuthorityError(
            f"runtime pins are not used by the closed import graph: {sorted(unused_pins)}"
        )

    literal_schema_paths: set[str] = set()
    for tree in trees.values():
        literal_schema_paths.update(
            _schema_literal_path(literal) for literal in _schema_literals(tree)
        )
    # A semantic schema root is executable contract authority even when no
    # Python string literal happens to name it.  Seed it into the same graph so
    # nested references cannot remain unhashed behind an apparently exact root.
    semantic_schema_paths = {
        relative for relative in semantics if relative.endswith(".schema.json")
    }
    referenced_schema_paths: set[str] = set()
    schema_queue = sorted(literal_schema_paths | semantic_schema_paths)
    parsed_schemas: set[str] = set()
    schema_identifiers: dict[str, str] = {}
    while schema_queue:
        relative = schema_queue.pop()
        if relative in parsed_schemas:
            continue
        path = _safe_file(root, relative)
        try:
            payload = json.loads(capture.read(relative).decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DependencyAuthorityError(
                f"cannot parse JSON-Schema dependency {relative}: {exc}"
            ) from exc
        parsed_schemas.add(relative)
        try:
            identifiers = schema_resource_ids(payload, path.as_uri())
        except LocalSchemaResolutionError as exc:
            raise DependencyAuthorityError(
                f"JSON-Schema identifier is invalid in {relative}: {exc}"
            ) from exc
        local_ids: set[str] = set()
        for schema_id in identifiers:
            prior = schema_identifiers.get(schema_id)
            if schema_id in local_ids or prior is not None:
                raise DependencyAuthorityError(
                    f"duplicate JSON-Schema $id {schema_id!r}: "
                    f"{prior or relative}, {relative}"
                )
            local_ids.add(schema_id)
            schema_identifiers[schema_id] = relative
        schema_roles: list[str] = []
        if relative in literal_schema_paths:
            schema_roles.append("json_schema_literal")
        if relative in semantic_schema_paths:
            schema_roles.append("json_schema_semantic_root")
        if schema_roles:
            add_path(relative, schema_roles)
        for reference in schema_document_references(payload):
            target = _schema_reference_path(root, relative, reference)
            if target is not None and target not in parsed_schemas:
                referenced_schema_paths.add(target)
                schema_queue.append(target)
                add_path(target, ("json_schema_reference",))

    runtime_versions = {
        distribution: _runtime_version(distribution)
        for distribution in sorted(set(distributions[module] for module in third_party_modules))
    }
    runtime_dependencies = [
        {"name": "python", "version": platform.python_version()},
        *[
            {"name": distribution, "version": version}
            for distribution, version in runtime_versions.items()
        ],
    ]
    third_party_boundary = [
        {
            "module": module,
            "distribution": distributions[module],
            "version": runtime_versions[distributions[module]],
        }
        for module in sorted(third_party_modules)
    ]
    declared_roots = [
        {"kind": "entry_python", "path": path, "roles": list(roles)}
        for path, roles in entries.items()
    ] + [
        {"kind": "semantic", "path": path, "roles": list(roles)}
        for path, roles in semantics.items()
    ]
    authority_entries = []
    for relative in sorted(path_roles):
        data = capture.read(relative)
        authority_entries.append(
            {
                "path": relative,
                "roles": sorted(path_roles[relative]),
                "byte_size": len(data),
                "content_digest": bytes_digest(data),
            }
        )
    capture.assert_stable()
    core: dict[str, Any] = {
        "authority_version": AUTHORITY_VERSION,
        "scope": scope,
        "declared_roots": declared_roots,
        "entries": authority_entries,
        "schema_closure": {
            "literal_paths": sorted(literal_schema_paths),
            "referenced_paths": sorted(referenced_schema_paths),
        },
        "import_boundary": {
            "policy": IMPORT_POLICY,
            "repository_local_python_paths": sorted(python_paths),
            "stdlib_modules": sorted(stdlib_modules),
            "third_party_modules": third_party_boundary,
        },
        "runtime_dependencies": runtime_dependencies,
        "authority_boundary": authority_boundary,
    }
    core["content_digest"] = canonical_digest(core)
    return CapturedDependencyAuthority(
        authority=core,
        materials=tuple(
            (relative, capture.read(relative)) for relative in sorted(path_roles)
        ),
    )


def build_dependency_authority(
    *,
    scope: str,
    entry_python_paths: Mapping[str, Sequence[str]],
    semantic_paths: Mapping[str, Sequence[str]],
    authority_boundary: str,
    repository_root: Path | str = ROOT,
    runtime_distributions: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Derive an authority solely from one race-checked immutable byte capture."""

    return capture_dependency_authority(
        scope=scope,
        entry_python_paths=entry_python_paths,
        semantic_paths=semantic_paths,
        authority_boundary=authority_boundary,
        repository_root=repository_root,
        runtime_distributions=runtime_distributions,
    ).authority


def validate_dependency_authority(
    record: Mapping[str, Any],
    *,
    scope: str,
    entry_python_paths: Mapping[str, Sequence[str]],
    semantic_paths: Mapping[str, Sequence[str]],
    authority_boundary: str,
    repository_root: Path | str = ROOT,
    runtime_distributions: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Rebuild a profile and reject any graph, byte, schema, or runtime drift."""

    expected = build_dependency_authority(
        scope=scope,
        entry_python_paths=entry_python_paths,
        semantic_paths=semantic_paths,
        authority_boundary=authority_boundary,
        repository_root=repository_root,
        runtime_distributions=runtime_distributions,
    )
    if dict(record) != expected:
        raise DependencyAuthorityError(
            "dependency authority differs from the exact bounded repository-local closure"
        )
    return expected


__all__ = [
    "AUTHORITY_VERSION",
    "CapturedDependencyAuthority",
    "DependencyAuthorityError",
    "IMPORT_POLICY",
    "build_dependency_authority",
    "capture_dependency_authority",
    "validate_dependency_authority",
]
