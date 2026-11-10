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
"""Profile-driven, content-addressed publication for canonical discovery cycles.

The engine owns storage and recovery invariants only.  A trusted caller supplies
the scientific validation profile directly; an index can never name code to be
dynamically imported.  Core identity is independent from derived evidence and
profile authority, so one immutable cycle can acquire new validation evidence
without colliding with its earlier evidence tree.
"""

from __future__ import annotations

import copy
import fcntl
import json
import os
import shutil
import stat
import tempfile
from collections.abc import Callable, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from types import CodeType
from typing import Any

from agentic_common import ROOT, rel

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    file_digest,
    safe_relative_path,
    validate_instance,
)


INDEX_NAME = "publication-index.json"
INDEX_DIRECTORY = "indexes"
BUNDLE_MANIFEST = "bundle-manifest.json"
EVIDENCE_MANIFEST = "evidence-manifest.json"
ARCHIVE_MANIFEST = "archive-manifest.json"
PROFILE_AUTHORITY_NAME = "validation-authority.json"
LOCK_NAME = ".publication.lock"
RESERVED_MANIFEST_NAMES = frozenset(
    {BUNDLE_MANIFEST, EVIDENCE_MANIFEST, ARCHIVE_MANIFEST}
)

CoreValidator = Callable[[Mapping[str, Any], Path], Mapping[str, Any]]
EvidenceBuilder = Callable[[Mapping[str, Any], Path], Mapping[str, bytes]]
EvidenceValidator = Callable[[Mapping[str, Any], Path, Path], Mapping[str, Any]]
AuthorityBuilder = Callable[[Path], Mapping[str, Any]]
PublicationFailpoint = Callable[[str], None]


class PublicationContractError(ContractError):
    """Publication-integrity failure with a stable machine reason code."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"publication[{reason_code}]: {message}")


@dataclass(frozen=True)
class PublicationSource:
    """One canonical core plus portable locators embedded inside its trees."""

    cycle_path: Path
    state_root: Path
    workspace: Path
    target_id: str
    run_id: str
    workspace_locators: Mapping[str, Path] = field(default_factory=dict)
    state_locators: Mapping[str, Path] = field(default_factory=dict)


@dataclass(frozen=True)
class PublicationProfile:
    """Trusted callbacks and their explicitly declared semantic policy inputs."""

    profile_id: str
    profile_version: str
    bundle_prefix: str
    authority_boundary: str
    build_authority: AuthorityBuilder
    validate_core: CoreValidator
    build_evidence: EvidenceBuilder
    validate_evidence: EvidenceValidator
    semantic_contract: Mapping[str, Any] = field(default_factory=dict)


def _json_bytes(payload: Any) -> bytes:
    return (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _same_object(first: os.stat_result, second: os.stat_result) -> bool:
    """Compare stable identity fields around one no-follow read."""

    return (
        first.st_dev,
        first.st_ino,
        stat.S_IFMT(first.st_mode),
        first.st_size,
        first.st_mtime_ns,
    ) == (
        second.st_dev,
        second.st_ino,
        stat.S_IFMT(second.st_mode),
        second.st_size,
        second.st_mtime_ns,
    )


def _read_regular_bytes(path: Path, label: str) -> bytes:
    """Read exact regular-file bytes without following a concurrent swap."""

    raw = _absolute(path)
    try:
        before = os.stat(raw, follow_symlinks=False)
    except FileNotFoundError as exc:
        raise PublicationContractError(
            "path_missing", f"{label} is unavailable: {raw}"
        ) from exc
    except OSError as exc:
        raise PublicationContractError(
            "path_unavailable", f"{label} is unavailable: {raw}"
        ) from exc
    if stat.S_ISLNK(before.st_mode):
        raise PublicationContractError(
            "path_symlink", f"{label} cannot be a symlink: {raw}"
        )
    if not stat.S_ISREG(before.st_mode):
        raise PublicationContractError(
            "path_not_regular_file", f"{label} must be a regular file: {raw}"
        )
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(raw, flags)
    except OSError as exc:
        raise PublicationContractError(
            "path_changed", f"{label} changed or became linked: {raw}"
        ) from exc
    try:
        opened = os.fstat(descriptor)
        if not _same_object(before, opened):
            raise PublicationContractError(
                "path_changed", f"{label} changed while it was opened: {raw}"
            )
        chunks: list[bytes] = []
        while chunk := os.read(descriptor, 1024 * 1024):
            chunks.append(chunk)
        after = os.fstat(descriptor)
        try:
            named_after = os.stat(raw, follow_symlinks=False)
        except OSError as exc:
            raise PublicationContractError(
                "path_changed", f"{label} changed while it was read: {raw}"
            ) from exc
        if not _same_object(opened, after) or not _same_object(after, named_after):
            raise PublicationContractError(
                "path_changed", f"{label} changed while it was read: {raw}"
            )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(_read_regular_bytes(path, label).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} must be a JSON object: {path}")
    return value


def _absolute(path: Path) -> Path:
    return path if path.is_absolute() else Path.cwd() / path


def _real_file(path: Path, label: str) -> Path:
    raw = _absolute(path)
    if raw.is_symlink():
        raise PublicationContractError(
            "path_symlink", f"{label} cannot be a symlink: {raw}"
        )
    if not os.path.lexists(raw):
        raise PublicationContractError("path_missing", f"{label} is absent: {raw}")
    if not raw.is_file():
        raise PublicationContractError(
            "path_not_regular_file", f"{label} must be a regular file: {raw}"
        )
    return raw.resolve()


def _real_directory(path: Path, label: str) -> Path:
    raw = _absolute(path)
    if raw.is_symlink():
        raise PublicationContractError(
            "path_symlink", f"{label} cannot be a symlink: {raw}"
        )
    if not os.path.lexists(raw):
        raise PublicationContractError("path_missing", f"{label} is absent: {raw}")
    if not raw.is_dir():
        raise PublicationContractError(
            "path_not_directory", f"{label} must be a directory: {raw}"
        )
    return raw.resolve()


def _publication_relative_path(raw: str, root: Path, label: str) -> Path:
    """Resolve one portable locator and classify every path failure stably.

    Lexical validation precedes component inspection so an unsafe ``..`` can
    never make the link check escape the publication root.  Component checks
    then reject both leaf and intermediate links before ``resolve`` is allowed
    to canonicalize the locator.
    """

    if Path(raw).is_absolute():
        raise PublicationContractError("path_absolute", f"{label} must be relative")
    try:
        relative = safe_relative_path(raw, forbid_latest=False)
    except ContractError as exc:
        raise PublicationContractError(
            "path_noncanonical", f"{label} is not a safe relative path: {raw!r}"
        ) from exc
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if os.path.lexists(cursor) and cursor.is_symlink():
            raise PublicationContractError(
                "path_symlink", f"{label} cannot traverse a symlink: {raw!r}"
            )
    try:
        return safe_relative_path(raw, root, forbid_latest=False)
    except ContractError as exc:
        raise PublicationContractError(
            "path_noncanonical", f"{label} escapes its publication root: {raw!r}"
        ) from exc


def _safe_tree_rows(
    root: Path, *, excluded_names: set[str] | None = None
) -> list[dict[str, Any]]:
    """Describe exact bytes while rejecting links, special files, and swaps.

    ``excluded_names`` applies at the manifest root only.  Nested files with a
    reserved basename remain hashed, rather than silently escaping identity.
    """

    root = _real_directory(root, "publication tree")
    excluded_root_names = excluded_names or set()
    rows: list[dict[str, Any]] = []

    def walk(directory_fd: int, prefix: Path, *, depth: int) -> None:
        initial_directory = os.fstat(directory_fd)
        with os.scandir(directory_fd) as iterator:
            names = sorted(entry.name for entry in iterator)
        for name in names:
            if depth == 0 and name in excluded_root_names:
                continue
            try:
                before = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            except OSError as exc:
                raise ContractError(
                    f"publication tree changed during traversal: {prefix / name}"
                ) from exc
            relative_path = prefix / name
            relative = relative_path.as_posix()
            # Keep this lexical: resolving against the root would follow the
            # link that the descriptor walk is responsible for classifying.
            safe_relative_path(relative, forbid_latest=False)
            if stat.S_ISDIR(before.st_mode):
                flags = os.O_RDONLY
                if hasattr(os, "O_DIRECTORY"):
                    flags |= os.O_DIRECTORY
                if hasattr(os, "O_NOFOLLOW"):
                    flags |= os.O_NOFOLLOW
                try:
                    child_fd = os.open(name, flags, dir_fd=directory_fd)
                except OSError as exc:
                    raise ContractError(
                        f"publication tree directory changed or became linked: {relative}"
                    ) from exc
                try:
                    if not _same_object(before, os.fstat(child_fd)):
                        raise ContractError(
                            f"publication tree directory changed while opened: {relative}"
                        )
                    walk(child_fd, relative_path, depth=depth + 1)
                finally:
                    os.close(child_fd)
            elif stat.S_ISREG(before.st_mode):
                flags = os.O_RDONLY
                if hasattr(os, "O_NOFOLLOW"):
                    flags |= os.O_NOFOLLOW
                try:
                    file_fd = os.open(name, flags, dir_fd=directory_fd)
                except OSError as exc:
                    raise ContractError(
                        f"publication tree file changed or became linked: {relative}"
                    ) from exc
                try:
                    opened = os.fstat(file_fd)
                    if not _same_object(before, opened):
                        raise ContractError(
                            f"publication tree file changed while opened: {relative}"
                        )
                    chunks: list[bytes] = []
                    while chunk := os.read(file_fd, 1024 * 1024):
                        chunks.append(chunk)
                    after = os.fstat(file_fd)
                    named_after = os.stat(
                        name, dir_fd=directory_fd, follow_symlinks=False
                    )
                    if not _same_object(opened, after) or not _same_object(
                        after, named_after
                    ):
                        raise ContractError(
                            f"publication tree file changed while read: {relative}"
                        )
                    encoded = b"".join(chunks)
                    rows.append(
                        {
                            "path": relative,
                            "sha256": bytes_digest(encoded),
                            "size_bytes": len(encoded),
                        }
                    )
                finally:
                    os.close(file_fd)
            else:
                if stat.S_ISLNK(before.st_mode):
                    raise PublicationContractError(
                        "source_symlink",
                        f"publication tree contains a symlink: {root / relative_path}",
                    )
                raise PublicationContractError(
                    "special_file",
                    "publication trees contain only regular files and directories: "
                    f"{root / relative_path}",
                )
        with os.scandir(directory_fd) as iterator:
            final_names = sorted(entry.name for entry in iterator)
        final_directory = os.fstat(directory_fd)
        if names != final_names or (
            initial_directory.st_dev,
            initial_directory.st_ino,
        ) != (final_directory.st_dev, final_directory.st_ino):
            raise ContractError(f"publication tree changed during traversal: {root / prefix}")

    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(root, flags)
    try:
        walk(descriptor, Path(), depth=0)
    finally:
        os.close(descriptor)
    return sorted(rows, key=lambda row: row["path"])


def _copy_tree_contents(source: Path, destination: Path) -> None:
    """Copy through no-follow descriptors so concurrent link swaps fail."""

    source = _real_directory(source, "publication source tree")
    destination.mkdir(parents=True, exist_ok=False)

    def copy_directory(source_fd: int, target_root: Path, prefix: Path) -> None:
        with os.scandir(source_fd) as iterator:
            names = sorted(entry.name for entry in iterator)
        for name in names:
            before = os.stat(name, dir_fd=source_fd, follow_symlinks=False)
            relative = (prefix / name).as_posix()
            target = target_root / name
            if stat.S_ISDIR(before.st_mode):
                flags = os.O_RDONLY
                if hasattr(os, "O_DIRECTORY"):
                    flags |= os.O_DIRECTORY
                if hasattr(os, "O_NOFOLLOW"):
                    flags |= os.O_NOFOLLOW
                try:
                    child_fd = os.open(name, flags, dir_fd=source_fd)
                except OSError as exc:
                    raise ContractError(
                        f"publication source directory changed or became linked: {relative}"
                    ) from exc
                try:
                    if not _same_object(before, os.fstat(child_fd)):
                        raise ContractError(
                            f"publication source directory changed while opened: {relative}"
                        )
                    target.mkdir()
                    copy_directory(child_fd, target, prefix / name)
                finally:
                    os.close(child_fd)
            elif stat.S_ISREG(before.st_mode):
                flags = os.O_RDONLY
                if hasattr(os, "O_NOFOLLOW"):
                    flags |= os.O_NOFOLLOW
                try:
                    file_fd = os.open(name, flags, dir_fd=source_fd)
                except OSError as exc:
                    raise ContractError(
                        f"publication source file changed or became linked: {relative}"
                    ) from exc
                try:
                    opened = os.fstat(file_fd)
                    if not _same_object(before, opened):
                        raise ContractError(
                            f"publication source file changed while opened: {relative}"
                        )
                    with target.open("xb") as stream:
                        while chunk := os.read(file_fd, 1024 * 1024):
                            stream.write(chunk)
                        stream.flush()
                        os.fsync(stream.fileno())
                    after = os.fstat(file_fd)
                    named_after = os.stat(
                        name, dir_fd=source_fd, follow_symlinks=False
                    )
                    if not _same_object(opened, after) or not _same_object(
                        after, named_after
                    ):
                        raise ContractError(
                            f"publication source file changed while copied: {relative}"
                        )
                finally:
                    os.close(file_fd)
            else:
                if stat.S_ISLNK(before.st_mode):
                    raise PublicationContractError(
                        "source_symlink",
                        "publication source contains a symlink or became linked: "
                        f"{source / prefix / name}",
                    )
                raise PublicationContractError(
                    "special_file",
                    "publication source contains a special file; only regular files "
                    f"and directories are allowed: {source / prefix / name}",
                )
        with os.scandir(source_fd) as iterator:
            if names != sorted(entry.name for entry in iterator):
                raise ContractError(
                    f"publication source changed while copied: {source / prefix}"
                )

    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(source, flags)
    try:
        copy_directory(descriptor, destination, Path())
    finally:
        os.close(descriptor)


def _copy_regular_tree(source: Path, destination: Path) -> list[dict[str, Any]]:
    """Copy one coherent source snapshot and prove source/destination equality."""

    expected = _safe_tree_rows(source)
    _copy_tree_contents(source, destination)
    if _safe_tree_rows(source) != expected or _safe_tree_rows(destination) != expected:
        raise ContractError("publication source changed while its snapshot was copied")
    return expected


def _write_file(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _write_json(path: Path, payload: Any) -> None:
    _write_file(path, _json_bytes(payload))


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fsync_tree(root: Path) -> None:
    for row in _safe_tree_rows(root):
        with (root / row["path"]).open("rb") as stream:
            os.fsync(stream.fileno())
    directories = sorted(
        (path for path in root.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for directory in directories:
        _fsync_directory(directory)
    _fsync_directory(root)


def _write_immutable_bytes(path: Path, encoded: bytes) -> bool:
    """Hard-link a complete file into place; accept only byte-identical replay."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            if path.is_symlink():
                raise PublicationContractError(
                    "path_symlink", f"immutable publication file is a symlink: {path}"
                )
            if not path.is_file():
                raise PublicationContractError(
                    "path_not_regular_file",
                    f"immutable publication path is not a regular file: {path}",
                )
            if path.read_bytes() != encoded:
                raise ContractError(f"immutable publication file conflicts: {path}")
            return False
        _fsync_directory(path.parent)
        return True
    finally:
        temporary.unlink(missing_ok=True)


def _atomic_pointer(path: Path, payload: Mapping[str, Any]) -> None:
    if os.path.lexists(path):
        if path.is_symlink():
            raise PublicationContractError(
                "path_symlink", f"publication index cannot be a symlink: {path}"
            )
        if not path.is_file():
            raise PublicationContractError(
                "path_not_regular_file",
                f"publication index must be a regular file: {path}",
            )
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
        _fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _prepare_publication_root(path: Path, *, create: bool) -> Path:
    raw = _absolute(path)
    if os.path.lexists(raw):
        if raw.is_symlink():
            raise PublicationContractError(
                "path_symlink", f"publication root cannot be a symlink: {raw}"
            )
        if not raw.is_dir():
            raise PublicationContractError(
                "path_not_directory",
                f"publication root must be a directory: {raw}",
            )
    if create:
        raw.mkdir(parents=True, exist_ok=True)
    if raw.exists():
        return raw.resolve()
    return raw.absolute()


def _storage_directory(root: Path, name: str, *, create: bool) -> Path:
    """Resolve one direct storage child without accepting a linked namespace."""

    candidate = root / name
    if os.path.lexists(candidate):
        if candidate.is_symlink():
            raise PublicationContractError(
                "path_symlink",
                f"publication storage directory cannot be a symlink: {candidate}",
            )
        if not candidate.is_dir():
            raise PublicationContractError(
                "path_not_directory",
                f"publication storage path must be a directory: {candidate}",
            )
    if create:
        candidate.mkdir(parents=False, exist_ok=True)
    if candidate.exists() and candidate.resolve().parent != root.resolve():
        raise PublicationContractError(
            "path_escape", f"publication storage directory escapes root: {candidate}"
        )
    return candidate


@contextmanager
def publication_lock(publication_root: Path):
    """Serialize immutable installs, history merge, snapshot, and pointer write."""

    root = _prepare_publication_root(publication_root, create=True)
    lock_path = root / LOCK_NAME
    if os.path.lexists(lock_path):
        if lock_path.is_symlink():
            raise PublicationContractError(
                "path_symlink", f"publication lock cannot be a symlink: {lock_path}"
            )
        if not lock_path.is_file():
            raise PublicationContractError(
                "path_not_regular_file",
                f"publication lock must be a regular file: {lock_path}",
            )
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        raise PublicationContractError(
            "path_changed", f"publication lock changed or became linked: {lock_path}"
        ) from exc
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield root
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _declared_path(cycle_path: Path, value: Any, *, directory: bool) -> Path:
    candidate = Path(str(value))
    raw = candidate if candidate.is_absolute() else cycle_path.parent / candidate
    label = "canonical cycle directory locator" if directory else "canonical cycle file locator"
    return _real_directory(raw, label) if directory else _real_file(raw, label)


def _portable_cycle(cycle_path: Path, state_root: Path) -> dict[str, Any]:
    cycle = _object(cycle_path, "canonical cycle")
    commit = _declared_path(cycle_path, cycle["commit_path"], directory=True)
    manifest = _declared_path(cycle_path, cycle["manifest_path"], directory=False)
    try:
        commit_relative = commit.relative_to(state_root)
        manifest_relative = manifest.relative_to(state_root)
    except ValueError as exc:
        raise PublicationContractError(
            "path_escape", "cycle commit self-location escapes its declared state root"
        ) from exc
    portable = copy.deepcopy(cycle)
    portable["transaction_root"] = "canonical-state"
    portable["commit_path"] = (Path("canonical-state") / commit_relative).as_posix()
    portable["manifest_path"] = (
        Path("canonical-state") / manifest_relative
    ).as_posix()
    return portable


def _published_at(cycle: Mapping[str, Any]) -> str:
    events = cycle.get("events", [])
    if not isinstance(events, list) or not events:
        raise ContractError("canonical cycle has no event time for publication")
    values = [
        str(row["occurred_at"])
        for row in events
        if isinstance(row, Mapping) and isinstance(row.get("occurred_at"), str)
    ]
    if not values:
        raise ContractError("canonical cycle events lack timestamps")
    return max(values)


def _contained_relative(child: Path, parent: Path, label: str) -> Path:
    raw = _absolute(child)
    if raw.is_symlink():
        raise PublicationContractError("path_symlink", f"{label} cannot be a symlink")
    if not os.path.lexists(raw):
        raise PublicationContractError("path_missing", f"{label} is absent: {raw}")
    try:
        return raw.resolve().relative_to(parent.resolve())
    except ValueError as exc:
        raise PublicationContractError(
            "path_escape", f"{label} must be contained by {parent}"
        ) from exc


def source_locators(source: PublicationSource) -> dict[str, Any]:
    cycle_path = _real_file(source.cycle_path, "cycle path")
    state_root = _real_directory(source.state_root, "state root")
    workspace = _real_directory(source.workspace, "workspace")
    locators: dict[str, Any] = {
        "cycle_path": cycle_path,
        "state_root": state_root,
        "workspace": workspace,
        "target_id": source.target_id,
        "run_id": source.run_id,
    }
    for name, path in sorted(source.workspace_locators.items()):
        _contained_relative(path, workspace, f"workspace locator {name}")
        locators[name] = _absolute(path).resolve()
    for name, path in sorted(source.state_locators.items()):
        _contained_relative(path, state_root, f"state locator {name}")
        locators[name] = _absolute(path).resolve()
    return locators


def _manifest_locators(source: PublicationSource) -> dict[str, str]:
    workspace = _real_directory(source.workspace, "workspace")
    state_root = _real_directory(source.state_root, "state root")
    result = {
        "cycle_path": "cycle-result.json",
        "state_root": "canonical-state",
        "workspace": "workspace",
    }
    for name, path in sorted(source.workspace_locators.items()):
        relative = _contained_relative(path, workspace, f"workspace locator {name}")
        result[name] = (Path("workspace") / relative).as_posix()
    for name, path in sorted(source.state_locators.items()):
        relative = _contained_relative(path, state_root, f"state locator {name}")
        result[name] = (Path("canonical-state") / relative).as_posix()
    return result


def _resolved_manifest_locators(
    bundle_root: Path, metadata: Mapping[str, Any]
) -> dict[str, Any]:
    values = metadata.get("locators")
    if not isinstance(values, Mapping):
        raise ContractError("bundle manifest lacks typed locators")
    result: dict[str, Any] = {
        "target_id": metadata.get("target_id"),
        "run_id": metadata.get("run_id"),
    }
    for name, value in values.items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise ContractError("bundle locators must be string mappings")
        resolved = _publication_relative_path(
            value, bundle_root, f"bundle locator {name}"
        )
        if not os.path.lexists(resolved):
            raise PublicationContractError(
                "path_missing", f"bundle locator {name} is absent: {value!r}"
            )
        result[name] = resolved
    return result


def _content_manifest(
    *,
    kind: str,
    content_id: str,
    created_utc: str,
    files: list[dict[str, Any]],
    metadata: Mapping[str, Any],
) -> dict[str, Any]:
    manifest = {
        "schema_version": "1.0.0",
        "manifest_kind": kind,
        "content_id": content_id,
        "content_digest": canonical_digest(files),
        "created_utc": created_utc,
        "files": files,
        "metadata": dict(metadata),
    }
    validate_instance(manifest, "canonical_discovery_content_manifest.schema.json")
    return manifest


def _validate_manifest(
    root: Path, manifest_name: str, *, expected_kind: str
) -> dict[str, Any]:
    root = _real_directory(root, f"{expected_kind} root")
    manifest = _object(root / manifest_name, f"{expected_kind} manifest")
    validate_instance(manifest, "canonical_discovery_content_manifest.schema.json")
    if manifest["manifest_kind"] != expected_kind:
        raise ContractError(f"publication manifest kind mismatch: {root}")
    rows = _safe_tree_rows(root, excluded_names={manifest_name})
    if manifest["files"] != rows or manifest["content_digest"] != canonical_digest(
        rows
    ):
        raise ContractError(f"publication content manifest is stale: {root}")
    return manifest


def _validate_authority_shape(authority: Mapping[str, Any]) -> dict[str, Any]:
    validated = copy.deepcopy(dict(authority))
    validate_instance(
        validated, "canonical_publication_profile_authority.schema.json"
    )
    payload = copy.deepcopy(validated)
    digest = payload.pop("content_digest", None)
    if digest != canonical_digest(payload):
        raise ContractError("publication profile authority digest mismatch")
    _validate_profile_authority_digests(validated)
    return validated


def _code_constant(value: Any) -> Any:
    """Project code constants without checkout paths or line-table noise."""

    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bytes):
        return {"bytes_digest": bytes_digest(value)}
    if isinstance(value, tuple):
        return {"tuple": [_code_constant(item) for item in value]}
    if isinstance(value, frozenset):
        items = [_code_constant(item) for item in value]
        return {
            "frozenset": sorted(
                items,
                key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")),
            )
        }
    if isinstance(value, CodeType):
        return {"code": _code_semantics(value)}
    return {"type": type(value).__qualname__, "representation": repr(value)}


def _code_semantics(code: CodeType) -> dict[str, Any]:
    """Describe callable semantics while excluding non-semantic locations."""

    return {
        "argcount": code.co_argcount,
        "posonlyargcount": code.co_posonlyargcount,
        "kwonlyargcount": code.co_kwonlyargcount,
        "flags": code.co_flags,
        "bytecode_digest": bytes_digest(code.co_code),
        "exception_table_digest": bytes_digest(code.co_exceptiontable),
        "constants": [_code_constant(value) for value in code.co_consts],
        "names": list(code.co_names),
        "varnames": list(code.co_varnames),
        "freevars": list(code.co_freevars),
        "cellvars": list(code.co_cellvars),
    }


def _authority_value(value: Any, *, seen: dict[int, str], path: str) -> Any:
    """Serialize a default or closure value without address-dependent ``repr``.

    Publication callbacks are trusted Python callables, but their behavior can
    depend on defaults and closure cells just as strongly as on bytecode.  This
    finite serializer accepts canonical containers, paths, code objects, and
    nested Python callables.  Unsupported process-local objects fail closed.
    """

    if value is None or isinstance(value, (bool, int, float, str)):
        return {"kind": "scalar", "value": value}
    if isinstance(value, bytes):
        return {
            "kind": "bytes",
            "size_bytes": len(value),
            "content_digest": bytes_digest(value),
        }
    if isinstance(value, Path):
        return {"kind": "path", "value": value.as_posix()}
    if isinstance(value, CodeType):
        code = _code_semantics(value)
        return {"kind": "code", "value": code, "content_digest": canonical_digest(code)}
    identity = id(value)
    if identity in seen:
        return {"kind": "cycle_reference", "path": seen[identity]}
    if callable(value):
        return {
            "kind": "callable",
            "authority": _callable_authority(value, path, seen=seen),
        }
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ContractError(f"publication authority mapping has a non-string key at {path}")
        seen[identity] = path
        try:
            return {
                "kind": "mapping",
                "items": {
                    key: _authority_value(child, seen=seen, path=f"{path}.{key}")
                    for key, child in sorted(value.items())
                },
            }
        finally:
            seen.pop(identity, None)
    if isinstance(value, (list, tuple, set, frozenset)):
        seen[identity] = path
        try:
            items = [
                _authority_value(child, seen=seen, path=f"{path}[{index}]")
                for index, child in enumerate(value)
            ]
            kind = type(value).__name__
            if isinstance(value, (set, frozenset)):
                items = sorted(
                    items,
                    key=lambda item: json.dumps(
                        item, sort_keys=True, separators=(",", ":")
                    ),
                )
            return {"kind": kind, "items": items}
        finally:
            seen.pop(identity, None)
    raise ContractError(
        "publication callable authority cannot canonically bind "
        f"{type(value).__qualname__} at {path}"
    )


def _callable_authority(
    callback: Callable[..., Any], role: str, *, seen: dict[int, str] | None = None
) -> dict[str, Any]:
    code = getattr(callback, "__code__", None)
    if not isinstance(code, CodeType):
        raise ContractError(f"publication profile {role} must be a Python callable")
    active = {} if seen is None else seen
    identity = id(callback)
    if identity in active:
        raise ContractError(f"publication callable cycle is unrooted at {role}")
    active[identity] = role
    code_authority = _code_semantics(code)
    defaults = _authority_value(
        callback.__defaults__ or (), seen=active, path=f"{role}.defaults"
    )
    keyword_defaults = _authority_value(
        callback.__kwdefaults__ or {},
        seen=active,
        path=f"{role}.keyword_defaults",
    )
    cells = callback.__closure__ or ()
    if len(cells) != len(code.co_freevars):
        active.pop(identity, None)
        raise ContractError(f"publication callable closure arity drift at {role}")
    closure_cells: list[dict[str, Any]] = []
    for name, cell in zip(code.co_freevars, cells, strict=True):
        try:
            contents = cell.cell_contents
        except ValueError:
            serialized = {"kind": "empty_cell"}
        else:
            serialized = _authority_value(
                contents, seen=active, path=f"{role}.closure.{name}"
            )
        closure_cells.append(
            {
                "name": name,
                "value": serialized,
                "value_digest": canonical_digest(serialized),
            }
        )
    core: dict[str, Any] = {
        "role": role,
        "module": str(getattr(callback, "__module__", "")),
        "qualname": str(getattr(callback, "__qualname__", "")),
        "code": code_authority,
        "code_digest": canonical_digest(code_authority),
        "defaults": defaults,
        "defaults_digest": canonical_digest(defaults),
        "keyword_defaults": keyword_defaults,
        "keyword_defaults_digest": canonical_digest(keyword_defaults),
        "closure_cells": closure_cells,
        "closure_cells_digest": canonical_digest(closure_cells),
    }
    core["identity_digest"] = canonical_digest(core)
    active.pop(identity, None)
    return core


def _validate_authority_value(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        if value.get("kind") == "callable":
            authority = value.get("authority")
            if not isinstance(authority, Mapping):
                raise ContractError(f"nested callable authority is absent at {path}")
            _validate_callable_authority(authority, path=f"{path}.authority")
        for key, child in value.items():
            _validate_authority_value(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _validate_authority_value(child, path=f"{path}[{index}]")


def _validate_callable_authority(authority: Mapping[str, Any], *, path: str) -> None:
    """Recompute every nested callable/default/closure digest exactly."""

    required = {
        "role",
        "module",
        "qualname",
        "code",
        "code_digest",
        "defaults",
        "defaults_digest",
        "keyword_defaults",
        "keyword_defaults_digest",
        "closure_cells",
        "closure_cells_digest",
        "identity_digest",
    }
    if set(authority) != required:
        raise ContractError(f"callable authority shape differs at {path}")
    if authority["code_digest"] != canonical_digest(authority["code"]):
        raise ContractError(f"callable code digest mismatch at {path}")
    if authority["defaults_digest"] != canonical_digest(authority["defaults"]):
        raise ContractError(f"callable defaults digest mismatch at {path}")
    if authority["keyword_defaults_digest"] != canonical_digest(
        authority["keyword_defaults"]
    ):
        raise ContractError(f"callable keyword-defaults digest mismatch at {path}")
    cells = authority["closure_cells"]
    if not isinstance(cells, list):
        raise ContractError(f"callable closure cells are malformed at {path}")
    for index, cell in enumerate(cells):
        if not isinstance(cell, Mapping) or set(cell) != {"name", "value", "value_digest"}:
            raise ContractError(f"callable closure cell is malformed at {path}[{index}]")
        if cell["value_digest"] != canonical_digest(cell["value"]):
            raise ContractError(f"callable closure value digest mismatch at {path}[{index}]")
        _validate_authority_value(cell["value"], path=f"{path}.closure[{index}]")
    if authority["closure_cells_digest"] != canonical_digest(cells):
        raise ContractError(f"callable closure digest mismatch at {path}")
    _validate_authority_value(authority["defaults"], path=f"{path}.defaults")
    _validate_authority_value(
        authority["keyword_defaults"], path=f"{path}.keyword_defaults"
    )
    unsigned = copy.deepcopy(dict(authority))
    identity_digest = unsigned.pop("identity_digest")
    if identity_digest != canonical_digest(unsigned):
        raise ContractError(f"callable identity digest mismatch at {path}")


def _validate_profile_authority_digests(authority: Mapping[str, Any]) -> None:
    """Recursively verify the dependency, semantic, and callable digest tree."""

    semantics = authority.get("profile_semantics")
    dependency_digest = authority.get("dependency_authority_digest")
    if semantics is None and dependency_digest is None:
        return  # Historical pre-semantic authority remains readable as history.
    if not isinstance(semantics, Mapping) or not isinstance(dependency_digest, str):
        raise ContractError("publication profile authority has a partial nested authority")
    dependency = copy.deepcopy(dict(authority))
    dependency.pop("content_digest", None)
    dependency.pop("dependency_authority_digest", None)
    dependency.pop("profile_semantics", None)
    if dependency_digest != canonical_digest(dependency):
        raise ContractError("publication dependency authority digest mismatch")
    contract = semantics.get("semantic_contract")
    if not isinstance(contract, Mapping) or semantics.get(
        "semantic_contract_digest"
    ) != canonical_digest(contract):
        raise ContractError("publication semantic-contract digest mismatch")
    callables = semantics.get("callables")
    if not isinstance(callables, Mapping):
        raise ContractError("publication callable authority set is malformed")
    expected_roles = {
        "build_authority",
        "validate_core",
        "build_evidence",
        "validate_evidence",
    }
    if set(callables) != expected_roles:
        raise ContractError("publication callable authority set differs")
    for role, callable_authority in callables.items():
        if not isinstance(callable_authority, Mapping):
            raise ContractError(f"publication callable authority is malformed for {role}")
        if callable_authority.get("role") != role:
            raise ContractError(
                f"publication callable authority role differs for {role}"
            )
        _validate_callable_authority(callable_authority, path=f"callables.{role}")
    semantic_unsigned = copy.deepcopy(dict(semantics))
    semantic_digest = semantic_unsigned.pop("content_digest", None)
    if semantic_digest != canonical_digest(semantic_unsigned):
        raise ContractError("publication profile semantic authority digest mismatch")


def _build_profile_authority(
    profile: PublicationProfile, authority_repository_root: Path
) -> dict[str, Any]:
    """Bind dependency bytes, callback code, and declared profile semantics."""

    dependency = copy.deepcopy(
        dict(profile.build_authority(authority_repository_root.resolve()))
    )
    dependency_digest = dependency.pop("content_digest", None)
    if dependency_digest != canonical_digest(dependency):
        raise ContractError("publication dependency authority digest mismatch")
    semantic_contract = copy.deepcopy(dict(profile.semantic_contract))
    semantics: dict[str, Any] = {
        "profile_id": profile.profile_id,
        "profile_version": profile.profile_version,
        "bundle_prefix": profile.bundle_prefix,
        "authority_boundary": profile.authority_boundary,
        "semantic_contract": semantic_contract,
        "semantic_contract_digest": canonical_digest(semantic_contract),
        "callables": {
            role: _callable_authority(getattr(profile, role), role)
            for role in (
                "build_authority",
                "validate_core",
                "build_evidence",
                "validate_evidence",
            )
        },
    }
    semantics["content_digest"] = canonical_digest(semantics)
    dependency["dependency_authority_digest"] = dependency_digest
    dependency["profile_semantics"] = semantics
    dependency["content_digest"] = canonical_digest(dependency)
    return _validate_authority_shape(dependency)


def _stage_core(
    destination: Path,
    *,
    source: PublicationSource,
    profile: PublicationProfile,
    authority_repository_root: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if os.path.lexists(destination):
        raise ContractError(f"core stage already exists: {destination}")
    destination.mkdir(parents=True)
    state_root = _real_directory(source.state_root, "state root")
    workspace = _real_directory(source.workspace, "workspace")
    _copy_regular_tree(state_root, destination / "canonical-state")
    _copy_regular_tree(workspace, destination / "workspace")
    portable = _portable_cycle(_real_file(source.cycle_path, "cycle path"), state_root)
    if portable.get("target_id") != source.target_id or portable.get("run_id") != source.run_id:
        raise ContractError("publication source target/run differs from its cycle")
    _write_json(destination / "cycle-result.json", portable)
    rows = _safe_tree_rows(destination)
    bundle_id = f"{profile.bundle_prefix}-{canonical_digest(rows).removeprefix('sha256:')}"
    manifest = _content_manifest(
        kind="canonical_discovery_bundle",
        content_id=bundle_id,
        created_utc=_published_at(portable),
        files=rows,
        metadata={
            "target_id": source.target_id,
            "run_id": source.run_id,
            "cycle_id": portable["cycle_id"],
            "commit_id": portable["commit_id"],
            "locators": _manifest_locators(source),
            "authority_boundary": portable["authority_boundary"],
        },
    )
    _write_json(destination / BUNDLE_MANIFEST, manifest)
    _validate_manifest(
        destination, BUNDLE_MANIFEST, expected_kind="canonical_discovery_bundle"
    )
    locators = _resolved_manifest_locators(destination, manifest["metadata"])
    profile.validate_core(locators, authority_repository_root)
    return manifest, locators


def _stage_evidence(
    destination: Path,
    *,
    bundle_root: Path,
    bundle_manifest: Mapping[str, Any],
    profile: PublicationProfile,
    profile_authority: Mapping[str, Any],
    authority_repository_root: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if os.path.lexists(destination):
        raise ContractError(f"evidence stage already exists: {destination}")
    destination.mkdir(parents=True)
    locators = _resolved_manifest_locators(bundle_root, bundle_manifest["metadata"])
    payloads = profile.build_evidence(locators, authority_repository_root)
    if not isinstance(payloads, Mapping) or not payloads:
        raise ContractError("publication profile emitted no evidence")
    reserved = {EVIDENCE_MANIFEST, PROFILE_AUTHORITY_NAME}
    for relative, encoded in sorted(payloads.items()):
        if not isinstance(relative, str) or relative in reserved:
            raise ContractError(f"unsafe or reserved evidence path: {relative!r}")
        path = safe_relative_path(relative, destination, forbid_latest=False)
        if not isinstance(encoded, bytes):
            raise ContractError(f"evidence payload must be bytes: {relative}")
        _write_file(path, encoded)
    _write_json(destination / PROFILE_AUTHORITY_NAME, profile_authority)
    rows = _safe_tree_rows(destination)
    evidence_metadata = {
        "bundle_id": bundle_manifest["content_id"],
        "target_id": bundle_manifest["metadata"]["target_id"],
        "run_id": bundle_manifest["metadata"]["run_id"],
        "profile_id": profile.profile_id,
        "profile_version": profile.profile_version,
        "profile_authority_digest": profile_authority["content_digest"],
        "authority_boundary": profile.authority_boundary,
    }
    evidence_id = _evidence_id(rows, evidence_metadata)
    manifest = _content_manifest(
        kind="canonical_discovery_evidence",
        content_id=evidence_id,
        created_utc=str(bundle_manifest["created_utc"]),
        files=rows,
        metadata=evidence_metadata,
    )
    _write_json(destination / EVIDENCE_MANIFEST, manifest)
    _validate_manifest(
        destination,
        EVIDENCE_MANIFEST,
        expected_kind="canonical_discovery_evidence",
    )
    profile.validate_evidence(locators, destination, authority_repository_root)
    return manifest, locators


def _evidence_id(
    rows: list[dict[str, Any]], metadata: Mapping[str, Any]
) -> str:
    """Bind evidence bytes and their profile/core interpretation separately."""

    digest = canonical_digest({"files": rows, "metadata": dict(metadata)})
    return f"evidence-{digest.removeprefix('sha256:')}"


def _remove_stage(path: Path) -> None:
    if path.exists():
        if not path.name.startswith(".stage-"):
            raise ContractError(f"refusing to remove non-staging path: {path}")
        shutil.rmtree(path)


def _publish_directory(stage: Path, destination: Path) -> bool:
    if os.path.lexists(destination):
        if destination.is_symlink():
            _remove_stage(stage)
            raise PublicationContractError(
                "path_symlink", f"immutable destination is a symlink: {destination}"
            )
        if not destination.is_dir():
            _remove_stage(stage)
            raise PublicationContractError(
                "path_not_directory",
                f"immutable destination must be a directory: {destination}",
            )
        if _safe_tree_rows(stage) != _safe_tree_rows(destination):
            _remove_stage(stage)
            raise ContractError(
                f"immutable publication destination conflicts: {destination}"
            )
        _remove_stage(stage)
        return False
    try:
        os.rename(stage, destination)
    except OSError:
        if (
            destination.is_dir()
            and not destination.is_symlink()
            and _safe_tree_rows(stage) == _safe_tree_rows(destination)
        ):
            _remove_stage(stage)
            return False
        _remove_stage(stage)
        raise
    _fsync_directory(destination.parent)
    return True


def _source_reference(path: Path) -> tuple[str, str]:
    resolved = _real_directory(path, "legacy source")
    try:
        return "repository_relative", resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return "external_absolute_origin", str(resolved)


def _archive_plan(
    legacy_bundle: Path | None, *, publication_root: Path, label: str
) -> list[dict[str, Any]]:
    if legacy_bundle is None:
        return []
    source = _real_directory(legacy_bundle, "legacy source")
    if os.path.lexists(source / ARCHIVE_MANIFEST):
        raise ContractError(
            "legacy source root reserves archive-manifest.json for the archive wrapper"
        )
    rows = _safe_tree_rows(source)
    digest = canonical_digest(rows)
    archive_id = f"legacy-{label}-{digest.removeprefix('sha256:')}"
    return [
        {
            "source": str(source),
            "source_tree_digest": digest,
            "file_count": len(rows),
            "size_bytes": sum(row["size_bytes"] for row in rows),
            "archive_id": archive_id,
            "destination": str(publication_root / "archive" / archive_id),
            "source_retained": True,
        }
    ]


def _archive_legacy(
    legacy_bundle: Path,
    *,
    publication_root: Path,
    created_utc: str,
    label: str,
) -> dict[str, Any]:
    source = _real_directory(legacy_bundle, "legacy source")
    if os.path.lexists(source / ARCHIVE_MANIFEST):
        raise ContractError(
            "legacy source root reserves archive-manifest.json for the archive wrapper"
        )
    source_rows = _safe_tree_rows(source)
    source_digest = canonical_digest(source_rows)
    archive_id = f"legacy-{label}-{source_digest.removeprefix('sha256:')}"
    archive_parent = _storage_directory(publication_root, "archive", create=True)
    destination = archive_parent / archive_id
    stage = Path(tempfile.mkdtemp(prefix=".stage-archive-", dir=destination.parent))
    try:
        shutil.rmtree(stage)
        _copy_regular_tree(source, stage)
        if _safe_tree_rows(stage) != source_rows:
            raise ContractError("legacy archive copy differs from retained source")
        locator_mode, source_path = _source_reference(legacy_bundle)
        manifest = _content_manifest(
            kind="legacy_archive",
            content_id=archive_id,
            created_utc=created_utc,
            files=source_rows,
            metadata={
                "source_path": source_path,
                "source_locator_mode": locator_mode,
                "source_tree_digest": source_digest,
                "source_retained": True,
                "authority": "historical_non_current",
            },
        )
        _write_json(stage / ARCHIVE_MANIFEST, manifest)
        _fsync_tree(stage)
        _publish_directory(stage, destination)
    except Exception:
        _remove_stage(stage)
        raise
    manifest = _validate_manifest(
        destination, ARCHIVE_MANIFEST, expected_kind="legacy_archive"
    )
    return {
        "archive_id": archive_id,
        "archive_path": destination.relative_to(publication_root).as_posix(),
        "archive_manifest_digest": file_digest(destination / ARCHIVE_MANIFEST),
        "source_path": manifest["metadata"]["source_path"],
        "source_locator_mode": manifest["metadata"]["source_locator_mode"],
        "source_tree_digest": source_digest,
        "source_retained": True,
    }


def _legacy_index_state(index: Mapping[str, Any]) -> dict[str, Any]:
    unsigned = copy.deepcopy(dict(index))
    digest = unsigned.pop("index_digest", None)
    if digest != canonical_digest(unsigned):
        raise ContractError("legacy publication index digest mismatch")
    current = index.get("current")
    history = index.get("history", [])
    archives = index.get("legacy_archives", [])
    if not isinstance(current, Mapping) or not isinstance(history, list):
        raise ContractError("legacy publication index is malformed")
    return {
        "history": [],
        "legacy_publications": [dict(current), *[dict(row) for row in history]],
        "legacy_archives": [dict(row) for row in archives],
    }


def _pointer_without_digest(pointer: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(pointer))
    value.pop("content_digest", None)
    return value


def _load_selected_snapshot(
    publication_root: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    index_path = publication_root / INDEX_NAME
    pointer = _object(index_path, "publication index pointer")
    if pointer.get("index_kind") == "canonical_discovery_publication_index":
        raise ContractError("legacy publication index is not a current v2 pointer")
    validate_instance(pointer, "canonical_discovery_publication_index.schema.json")
    if pointer.get("index_kind") != "canonical_discovery_publication_pointer":
        raise ContractError("publication index is not a current pointer")
    if pointer["content_digest"] != canonical_digest(_pointer_without_digest(pointer)):
        raise ContractError("publication index pointer digest mismatch")
    snapshot_path = pointer["snapshot_path"]
    expected = (
        Path(INDEX_DIRECTORY)
        / f"index-{pointer['snapshot_sha256'].removeprefix('sha256:')}.json"
    ).as_posix()
    if snapshot_path != expected:
        raise ContractError("publication snapshot path is not content-addressed")
    resolved = _publication_relative_path(
        snapshot_path, publication_root, "publication snapshot"
    )
    if (
        file_digest(resolved) != pointer["snapshot_sha256"]
        or resolved.stat().st_size != pointer["snapshot_size_bytes"]
    ):
        raise ContractError("publication snapshot byte binding mismatch")
    snapshot = _object(resolved, "publication index snapshot")
    validate_instance(snapshot, "canonical_discovery_publication_index.schema.json")
    if snapshot.get("index_kind") != "canonical_discovery_publication_snapshot":
        raise ContractError("publication snapshot kind mismatch")
    _validate_history_invariants(snapshot)
    current = snapshot["current"]
    if (
        pointer["current_bundle_id"] != current["bundle_id"]
        or pointer["current_evidence_id"] != current["evidence_id"]
    ):
        raise ContractError("publication pointer selects different current IDs")
    return snapshot, pointer


def _load_previous_state(publication_root: Path) -> dict[str, Any]:
    index_path = publication_root / INDEX_NAME
    if not os.path.lexists(index_path):
        return {"history": [], "legacy_publications": [], "legacy_archives": []}
    if index_path.is_symlink():
        raise PublicationContractError(
            "path_symlink", "publication index cannot be a symlink"
        )
    index = _object(index_path, "publication index")
    if index.get("index_kind") == "canonical_discovery_publication_index":
        return _legacy_index_state(index)
    snapshot, _ = _load_selected_snapshot(publication_root)
    return {
        "history": list(snapshot["history"]),
        "legacy_publications": list(snapshot["legacy_publications"]),
        "legacy_archives": list(snapshot["legacy_archives"]),
        "current": dict(snapshot["current"]),
    }


def plan_profile_publication(
    *,
    source: PublicationSource,
    profile: PublicationProfile,
    publication_root: Path,
    legacy_bundle: Path | None = None,
    legacy_label: str = "prior-publication",
    authority_repository_root: Path = ROOT,
) -> dict[str, Any]:
    """Return exact IDs and destinations without writing below publication_root."""

    root = _prepare_publication_root(publication_root, create=False)
    original = source_locators(source)
    core_validation = dict(
        profile.validate_core(original, authority_repository_root.resolve())
    )
    authority = _build_profile_authority(profile, authority_repository_root)
    with tempfile.TemporaryDirectory(prefix="canonical-publication-plan-") as temporary:
        stage_root = Path(temporary)
        bundle_manifest, _ = _stage_core(
            stage_root / "bundle",
            source=source,
            profile=profile,
            authority_repository_root=authority_repository_root.resolve(),
        )
        evidence_manifest, _ = _stage_evidence(
            stage_root / "evidence",
            bundle_root=stage_root / "bundle",
            bundle_manifest=bundle_manifest,
            profile=profile,
            profile_authority=authority,
            authority_repository_root=authority_repository_root.resolve(),
        )
    bundle_id = bundle_manifest["content_id"]
    evidence_id = evidence_manifest["content_id"]
    return {
        "schema_version": "2.0.0",
        "operation": "plan_only_no_persistent_writes",
        "publication_root": str(root),
        "bundle_id": bundle_id,
        "bundle_content_digest": bundle_manifest["content_digest"],
        "bundle_file_count": len(bundle_manifest["files"]),
        "bundle_size_bytes": sum(row["size_bytes"] for row in bundle_manifest["files"]),
        "bundle_destination": str(root / "publications" / bundle_id),
        "evidence_id": evidence_id,
        "evidence_content_digest": evidence_manifest["content_digest"],
        "evidence_file_count": len(evidence_manifest["files"]),
        "evidence_size_bytes": sum(
            row["size_bytes"] for row in evidence_manifest["files"]
        ),
        "evidence_destination": str(root / "evidence" / evidence_id),
        "index_destination": str(root / INDEX_NAME),
        "target_id": source.target_id,
        "run_id": source.run_id,
        "cycle_id": bundle_manifest["metadata"]["cycle_id"],
        "commit_id": bundle_manifest["metadata"]["commit_id"],
        "profile_id": profile.profile_id,
        "profile_version": profile.profile_version,
        "profile_authority_digest": authority["content_digest"],
        "bundle_manifest_sha256": bytes_digest(_json_bytes(bundle_manifest)),
        "evidence_manifest_sha256": bytes_digest(_json_bytes(evidence_manifest)),
        "core_validation_status": core_validation.get("status"),
        "legacy_archives": _archive_plan(
            legacy_bundle, publication_root=root, label=legacy_label
        ),
    }


def _current_row(
    *,
    plan: Mapping[str, Any],
    bundle_root: Path,
    evidence_root: Path,
    bundle_manifest: Mapping[str, Any],
    evidence_manifest: Mapping[str, Any],
    profile: PublicationProfile,
    publication_root: Path,
) -> dict[str, Any]:
    return {
        "bundle_id": plan["bundle_id"],
        "bundle_path": bundle_root.relative_to(publication_root).as_posix(),
        "evidence_id": plan["evidence_id"],
        "evidence_path": evidence_root.relative_to(publication_root).as_posix(),
        "bundle_manifest_digest": file_digest(bundle_root / BUNDLE_MANIFEST),
        "evidence_manifest_digest": file_digest(evidence_root / EVIDENCE_MANIFEST),
        "target_id": plan["target_id"],
        "run_id": plan["run_id"],
        "cycle_id": bundle_manifest["metadata"]["cycle_id"],
        "commit_id": bundle_manifest["metadata"]["commit_id"],
        "profile_id": profile.profile_id,
        "profile_version": profile.profile_version,
        "profile_authority_digest": evidence_manifest["metadata"][
            "profile_authority_digest"
        ],
        "published_utc": bundle_manifest["created_utc"],
    }


def publish_profile_current(
    *,
    source: PublicationSource,
    profile: PublicationProfile,
    publication_root: Path,
    legacy_bundle: Path | None = None,
    legacy_label: str = "prior-publication",
    authority_repository_root: Path = ROOT,
    failpoint: PublicationFailpoint | None = None,
) -> dict[str, Any]:
    """Validate a complete candidate before the byte-exact pointer transition."""

    plan = plan_profile_publication(
        source=source,
        profile=profile,
        publication_root=publication_root,
        legacy_bundle=legacy_bundle,
        legacy_label=legacy_label,
        authority_repository_root=authority_repository_root,
    )
    if failpoint is not None:
        failpoint("after_plan")
    authority = _build_profile_authority(profile, authority_repository_root)
    if authority["content_digest"] != plan["profile_authority_digest"]:
        raise ContractError("publication profile authority has drifted after planning")
    with publication_lock(publication_root) as root:
        previous = _load_previous_state(root)
        bundle_parent = _storage_directory(root, "publications", create=True)
        evidence_parent = _storage_directory(root, "evidence", create=True)
        core_stage = Path(
            tempfile.mkdtemp(prefix=".stage-bundle-", dir=bundle_parent)
        )
        shutil.rmtree(core_stage)
        try:
            bundle_manifest, _ = _stage_core(
                core_stage,
                source=source,
                profile=profile,
                authority_repository_root=authority_repository_root.resolve(),
            )
            if (
                bundle_manifest["content_id"] != plan["bundle_id"]
                or bytes_digest(_json_bytes(bundle_manifest))
                != plan["bundle_manifest_sha256"]
            ):
                raise ContractError("source changed after publication planning")
            bundle_root = root / "publications" / plan["bundle_id"]
            _fsync_tree(core_stage)
            core_created = _publish_directory(core_stage, bundle_root)
            if failpoint is not None:
                failpoint("after_bundle_install")
        except Exception:
            _remove_stage(core_stage)
            raise
        evidence_stage = Path(
            tempfile.mkdtemp(prefix=".stage-evidence-", dir=evidence_parent)
        )
        shutil.rmtree(evidence_stage)
        try:
            evidence_manifest, _ = _stage_evidence(
                evidence_stage,
                bundle_root=bundle_root,
                bundle_manifest=bundle_manifest,
                profile=profile,
                profile_authority=authority,
                authority_repository_root=authority_repository_root.resolve(),
            )
            if (
                evidence_manifest["content_id"] != plan["evidence_id"]
                or bytes_digest(_json_bytes(evidence_manifest))
                != plan["evidence_manifest_sha256"]
            ):
                raise ContractError("evidence changed after publication planning")
            evidence_root = root / "evidence" / plan["evidence_id"]
            _fsync_tree(evidence_stage)
            evidence_created = _publish_directory(evidence_stage, evidence_root)
            if failpoint is not None:
                failpoint("after_evidence_install")
        except Exception:
            _remove_stage(evidence_stage)
            raise
        archives: list[dict[str, Any]] = []
        if legacy_bundle is not None:
            archives.append(
                _archive_legacy(
                    legacy_bundle,
                    publication_root=root,
                    created_utc=bundle_manifest["created_utc"],
                    label=legacy_label,
                )
            )
        if failpoint is not None:
            failpoint("after_archive_install")
        current = _current_row(
            plan=plan,
            bundle_root=bundle_root,
            evidence_root=evidence_root,
            bundle_manifest=bundle_manifest,
            evidence_manifest=evidence_manifest,
            profile=profile,
            publication_root=root,
        )
        history = list(previous.get("history", []))
        prior_current = previous.get("current")
        if (
            prior_current
            and _publication_identity(prior_current) != _publication_identity(current)
        ):
            history.append(prior_current)
        history = [
            row
            for row in history
            if _publication_identity(row) != _publication_identity(current)
        ]
        if len({_publication_identity(row) for row in history}) != len(history):
            raise ContractError("publication history contains duplicate identities")
        legacy_archives = list(previous.get("legacy_archives", []))
        for archive in archives:
            if archive not in legacy_archives:
                legacy_archives.append(archive)
        snapshot = {
            "schema_version": "2.0.0",
            "index_kind": "canonical_discovery_publication_snapshot",
            "current": current,
            "history": history,
            "legacy_publications": list(previous.get("legacy_publications", [])),
            "legacy_archives": legacy_archives,
            "authority_boundary": (
                "The mutable pointer selects one immutable index snapshot; that snapshot "
                "selects one exact core/evidence/profile tuple. History is non-current."
            ),
        }
        validate_instance(snapshot, "canonical_discovery_publication_index.schema.json")
        snapshot_bytes = _json_bytes(snapshot)
        snapshot_sha256 = bytes_digest(snapshot_bytes)
        snapshot_relative = (
            Path(INDEX_DIRECTORY)
            / f"index-{snapshot_sha256.removeprefix('sha256:')}.json"
        ).as_posix()
        snapshot_path = _storage_directory(root, INDEX_DIRECTORY, create=True) / Path(
            snapshot_relative
        ).name
        snapshot_created = _write_immutable_bytes(snapshot_path, snapshot_bytes)
        if failpoint is not None:
            failpoint("after_snapshot_install")
        pointer: dict[str, Any] = {
            "schema_version": "2.0.0",
            "index_kind": "canonical_discovery_publication_pointer",
            "snapshot_path": snapshot_relative,
            "snapshot_sha256": snapshot_sha256,
            "snapshot_size_bytes": len(snapshot_bytes),
            "current_bundle_id": current["bundle_id"],
            "current_evidence_id": current["evidence_id"],
        }
        pointer["content_digest"] = canonical_digest(pointer)
        validate_instance(pointer, "canonical_discovery_publication_index.schema.json")
        index_path = root / INDEX_NAME
        old_bytes = (
            index_path.read_bytes()
            if index_path.is_file() and not index_path.is_symlink()
            else None
        )
        new_bytes = _json_bytes(pointer)
        candidate = _validate_snapshot(
            snapshot,
            root,
            profile=profile,
            authority_repository_root=authority_repository_root,
        )
        if failpoint is not None:
            failpoint("before_pointer_replace")
        pointer_changed = old_bytes != new_bytes
        try:
            if pointer_changed:
                _atomic_pointer(index_path, pointer)
            if failpoint is not None:
                failpoint("after_pointer_replace")
            selected_snapshot, selected_pointer = _load_selected_snapshot(root)
            if selected_snapshot != snapshot or selected_pointer != pointer:
                raise ContractError("publication pointer did not select the validated snapshot")
        except Exception:
            if pointer_changed:
                _restore_pointer_bytes(index_path, old_bytes)
            raise
        return {
            **candidate,
            "snapshot_sha256": snapshot_sha256,
            "core_created": core_created,
            "evidence_created": evidence_created,
            "snapshot_created": snapshot_created,
            "index_updated": pointer_changed,
            "plan": plan,
        }


def _restore_pointer_bytes(path: Path, prior: bytes | None) -> None:
    """Restore the exact pre-call pointer (or its absence) under the root lock."""

    if prior is None:
        if os.path.lexists(path):
            if path.is_symlink():
                raise PublicationContractError(
                    "path_symlink", f"cannot remove linked failed pointer: {path}"
                )
            if not path.is_file():
                raise PublicationContractError(
                    "path_not_regular_file",
                    f"cannot remove non-file failed pointer: {path}",
                )
            path.unlink()
            _fsync_directory(path.parent)
        return
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.rollback-", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(prior)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _safe_index_path(root: Path, relative: str, expected: Path) -> Path:
    resolved = _publication_relative_path(
        relative, root, "publication index locator"
    )
    if resolved != expected.resolve():
        raise PublicationContractError(
            "path_noncanonical", "publication index locator is non-canonical"
        )
    return resolved


def _validate_row(
    row: Mapping[str, Any], publication_root: Path, *, profile: PublicationProfile | None
) -> tuple[Path, Path, dict[str, Any], dict[str, Any]]:
    bundle_root = _safe_index_path(
        publication_root,
        str(row["bundle_path"]),
        publication_root / "publications" / str(row["bundle_id"]),
    )
    evidence_root = _safe_index_path(
        publication_root,
        str(row["evidence_path"]),
        publication_root / "evidence" / str(row["evidence_id"]),
    )
    bundle_manifest = _validate_manifest(
        bundle_root, BUNDLE_MANIFEST, expected_kind="canonical_discovery_bundle"
    )
    evidence_manifest = _validate_manifest(
        evidence_root,
        EVIDENCE_MANIFEST,
        expected_kind="canonical_discovery_evidence",
    )
    bundle_digest = bundle_manifest["content_digest"].removeprefix("sha256:")
    if bundle_manifest["content_id"] != row["bundle_id"] or not str(
        row["bundle_id"]
    ).endswith(bundle_digest):
        raise ContractError("publication bundle is not content-addressed")
    if evidence_manifest["content_id"] != row["evidence_id"] or row[
        "evidence_id"
    ] != _evidence_id(evidence_manifest["files"], evidence_manifest["metadata"]):
        raise ContractError("publication evidence is not content-addressed")
    if (
        file_digest(bundle_root / BUNDLE_MANIFEST)
        != row["bundle_manifest_digest"]
        or file_digest(evidence_root / EVIDENCE_MANIFEST)
        != row["evidence_manifest_digest"]
    ):
        raise ContractError("publication manifest digest mismatch")
    metadata = bundle_manifest["metadata"]
    evidence_metadata = evidence_manifest["metadata"]
    exact = {
        "target_id": metadata.get("target_id"),
        "run_id": metadata.get("run_id"),
        "cycle_id": metadata.get("cycle_id"),
        "commit_id": metadata.get("commit_id"),
        "profile_id": evidence_metadata.get("profile_id"),
        "profile_version": evidence_metadata.get("profile_version"),
        "profile_authority_digest": evidence_metadata.get(
            "profile_authority_digest"
        ),
    }
    if any(row.get(name) != value for name, value in exact.items()):
        raise ContractError("publication row differs from manifest metadata")
    if evidence_metadata.get("bundle_id") != row["bundle_id"]:
        raise ContractError("evidence is bound to a different core")
    published_authority = _validate_authority_shape(
        _object(evidence_root / PROFILE_AUTHORITY_NAME, "published profile authority")
    )
    if published_authority["content_digest"] != row["profile_authority_digest"]:
        raise ContractError("publication row differs from its profile authority")
    if profile is not None:
        if (
            row["profile_id"] != profile.profile_id
            or row["profile_version"] != profile.profile_version
            or row["bundle_id"] != f"{profile.bundle_prefix}-{bundle_digest}"
        ):
            raise ContractError("current publication uses a different trusted profile")
    return bundle_root, evidence_root, bundle_manifest, evidence_manifest


def _validate_legacy_publication(row: Mapping[str, Any], root: Path) -> None:
    bundle_id = str(row.get("bundle_id") or "")
    bundle = _safe_index_path(
        root,
        str(row.get("bundle_path") or ""),
        root / "publications" / bundle_id,
    )
    evidence = _safe_index_path(
        root,
        str(row.get("evidence_path") or ""),
        root / "evidence" / bundle_id,
    )
    bundle_manifest = _validate_manifest(
        bundle, BUNDLE_MANIFEST, expected_kind="canonical_discovery_bundle"
    )
    evidence_manifest = _validate_manifest(
        evidence, EVIDENCE_MANIFEST, expected_kind="canonical_discovery_evidence"
    )
    bundle_digest = bundle_manifest["content_digest"].removeprefix("sha256:")
    if (
        bundle_manifest["content_id"] != bundle_id
        or not bundle_id.endswith(bundle_digest)
        or file_digest(bundle / BUNDLE_MANIFEST)
        != row.get("bundle_manifest_digest")
        or file_digest(evidence / EVIDENCE_MANIFEST)
        != row.get("evidence_manifest_digest")
        or evidence_manifest["metadata"].get("bundle_id") != bundle_id
    ):
        raise ContractError("legacy publication row is not exactly bound")


def _resolve_source_path(archive: Mapping[str, Any]) -> Path:
    value = Path(str(archive["source_path"]))
    mode = archive.get("source_locator_mode")
    if mode == "repository_relative" or (mode is None and not value.is_absolute()):
        return ROOT / value
    if mode == "external_absolute_origin" or (mode is None and value.is_absolute()):
        return value
    raise ContractError("legacy archive source locator mode is unknown")


def _validate_archives(archives: list[Any], root: Path) -> None:
    for raw in archives:
        if not isinstance(raw, Mapping):
            raise ContractError("legacy archive row is malformed")
        archive = dict(raw)
        archive_root = _safe_index_path(
            root,
            str(archive["archive_path"]),
            root / "archive" / str(archive["archive_id"]),
        )
        manifest = _validate_manifest(
            archive_root, ARCHIVE_MANIFEST, expected_kind="legacy_archive"
        )
        source = _resolve_source_path(archive)
        source_rows = _safe_tree_rows(source)
        metadata = manifest["metadata"]
        if (
            manifest["content_id"] != archive["archive_id"]
            or manifest["content_digest"] != archive["source_tree_digest"]
            or file_digest(archive_root / ARCHIVE_MANIFEST)
            != archive["archive_manifest_digest"]
            or canonical_digest(source_rows) != archive["source_tree_digest"]
            or manifest["files"] != source_rows
            or metadata.get("source_path") != archive.get("source_path")
            or metadata.get("source_locator_mode")
            != archive.get("source_locator_mode")
            or metadata.get("source_tree_digest")
            != archive.get("source_tree_digest")
            or metadata.get("source_retained") is not True
            or archive.get("source_retained") is not True
        ):
            raise ContractError("legacy archive/source-retention binding mismatch")


def _publication_identity(row: Mapping[str, Any]) -> tuple[str, str]:
    """Identify a version by independent core and evidence identities."""

    return str(row.get("bundle_id")), str(row.get("evidence_id"))


def _validate_history_invariants(snapshot: Mapping[str, Any]) -> None:
    current = _publication_identity(snapshot["current"])
    history = [_publication_identity(row) for row in snapshot["history"]]
    if current in history:
        raise ContractError("publication history must be disjoint from current")
    if len(history) != len(set(history)):
        raise ContractError("publication history contains duplicate identities")


def _validate_snapshot(
    snapshot: Mapping[str, Any],
    root: Path,
    *,
    profile: PublicationProfile,
    authority_repository_root: Path,
) -> dict[str, Any]:
    """Replay every candidate edge before it may become current authority."""

    validate_instance(snapshot, "canonical_discovery_publication_index.schema.json")
    if snapshot.get("index_kind") != "canonical_discovery_publication_snapshot":
        raise ContractError("publication candidate is not an index snapshot")
    _validate_history_invariants(snapshot)
    current = snapshot["current"]
    bundle, evidence, bundle_manifest, evidence_manifest = _validate_row(
        current, root, profile=profile
    )
    locators = _resolved_manifest_locators(bundle, bundle_manifest["metadata"])
    current_authority = _build_profile_authority(profile, authority_repository_root)
    published_authority = _validate_authority_shape(
        _object(evidence / PROFILE_AUTHORITY_NAME, "published profile authority")
    )
    if (
        published_authority != current_authority
        or current_authority["content_digest"]
        != current["profile_authority_digest"]
    ):
        raise ContractError("current publication profile authority has drifted")
    core_validation = dict(
        profile.validate_core(locators, authority_repository_root.resolve())
    )
    evidence_validation = dict(
        profile.validate_evidence(
            locators, evidence, authority_repository_root.resolve()
        )
    )
    for row in snapshot["history"]:
        _validate_row(row, root, profile=None)
    for row in snapshot["legacy_publications"]:
        _validate_legacy_publication(row, root)
    _validate_archives(snapshot["legacy_archives"], root)
    return {
        "schema_version": "2.0.0",
        "status": "passed",
        "bundle_id": current["bundle_id"],
        "evidence_id": current["evidence_id"],
        "target_id": current["target_id"],
        "run_id": current["run_id"],
        "cycle_id": current["cycle_id"],
        "commit_id": current["commit_id"],
        "profile_id": current["profile_id"],
        "profile_version": current["profile_version"],
        "profile_authority_digest": current["profile_authority_digest"],
        "bundle_content_digest": bundle_manifest["content_digest"],
        "evidence_content_digest": evidence_manifest["content_digest"],
        "history_count": len(snapshot["history"]),
        "legacy_publication_count": len(snapshot["legacy_publications"]),
        "legacy_archive_count": len(snapshot["legacy_archives"]),
        "core_validation": core_validation,
        "evidence_validation": evidence_validation,
    }


def resolve_profile_current(
    *, publication_root: Path, profile: PublicationProfile
) -> dict[str, Any]:
    root = _prepare_publication_root(publication_root, create=False)
    if not root.is_dir():
        raise PublicationContractError(
            "path_missing", f"publication root does not exist: {root}"
        )
    snapshot, pointer = _load_selected_snapshot(root)
    current = snapshot["current"]
    bundle, evidence, manifest, evidence_manifest = _validate_row(
        current, root, profile=profile
    )
    locators = _resolved_manifest_locators(bundle, manifest["metadata"])
    return {
        "bundle_id": current["bundle_id"],
        "evidence_id": current["evidence_id"],
        "publication_root": root,
        "index_path": root / INDEX_NAME,
        "snapshot_path": _publication_relative_path(
            pointer["snapshot_path"], root, "publication snapshot"
        ),
        "bundle_root": bundle,
        "evidence_root": evidence,
        "bundle_manifest": manifest,
        "evidence_manifest": evidence_manifest,
        **locators,
    }


def validate_profile_current(
    *,
    publication_root: Path,
    profile: PublicationProfile,
    authority_repository_root: Path = ROOT,
) -> dict[str, Any]:
    root = _prepare_publication_root(publication_root, create=False)
    snapshot, pointer = _load_selected_snapshot(root)
    result = _validate_snapshot(
        snapshot,
        root,
        profile=profile,
        authority_repository_root=authority_repository_root,
    )
    return {**result, "snapshot_sha256": pointer["snapshot_sha256"]}


__all__ = [
    "ARCHIVE_MANIFEST",
    "BUNDLE_MANIFEST",
    "EVIDENCE_MANIFEST",
    "INDEX_NAME",
    "PROFILE_AUTHORITY_NAME",
    "PublicationContractError",
    "PublicationProfile",
    "PublicationSource",
    "PublicationFailpoint",
    "_safe_tree_rows",
    "plan_profile_publication",
    "publication_lock",
    "publish_profile_current",
    "resolve_profile_current",
    "source_locators",
    "validate_profile_current",
]
