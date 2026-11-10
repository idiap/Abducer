# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Bounded no-follow I/O shared by the causal byte materializer v3.

This module is intentionally standard-library-only so the worker and validator
have a small, derivable executable closure.  Evidence paths are opened one
component at a time below an already selected workspace directory.  Symlinks,
hardlinks, special files, oversized files, noncanonical paths, and read growth
all fail before their bytes can acquire protocol authority.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import stat
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


MAX_ARTIFACT_BYTES = 8 * 1024 * 1024
MAX_REQUEST_BYTES = 256 * 1024
MAX_RECEIPT_BYTES = 1024 * 1024
MAX_BINDING_BYTES = 4 * 1024 * 1024
MAX_PATH_BYTES = 512
MAX_ATTEMPTS = 32
SUBPROCESS_TIMEOUT_SECONDS = 30
JSON_MEDIA_TYPE = "application/json"


class CausalMaterializerIOError(ValueError):
    """Raised when bounded immutable materializer I/O cannot be established."""


def canonical_json_bytes(value: Any) -> bytes:
    """Encode one JSON value with the repository's canonical JSON convention."""

    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise CausalMaterializerIOError(
            f"value is not canonical-JSON encodable: {exc}"
        ) from exc
    return text.encode("utf-8")


def tagged_sha256(data: bytes) -> str:
    """Return the tagged exact-byte digest used by discovery contracts."""

    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_relative_path(raw: str) -> str:
    """Return one bounded canonical POSIX path below the workspace."""

    if (
        not isinstance(raw, str)
        or not raw
        or "\\" in raw
        or len(raw.encode("utf-8")) > MAX_PATH_BYTES
    ):
        raise CausalMaterializerIOError("evidence path is empty, noncanonical, or too long")
    relative = PurePosixPath(raw)
    if (
        relative.is_absolute()
        or relative.as_posix() != raw
        or any(part in {"", ".", "..", "latest", "current"} for part in relative.parts)
    ):
        raise CausalMaterializerIOError(f"unsafe evidence path: {raw!r}")
    return raw


def _workspace_root(workspace: Path) -> Path:
    root = Path(workspace)
    if root.is_symlink() or not root.is_dir():
        raise CausalMaterializerIOError(
            "materializer workspace must be one existing non-symlink directory"
        )
    return root.resolve(strict=True)


def _open_flags(*, directory: bool, writable: bool = False) -> int:
    if not hasattr(os, "O_NOFOLLOW") or (directory and not hasattr(os, "O_DIRECTORY")):
        raise CausalMaterializerIOError(
            "host cannot enforce no-follow component-safe materializer I/O"
        )
    flags = (os.O_RDWR if writable else os.O_RDONLY) | os.O_CLOEXEC | os.O_NOFOLLOW
    if directory:
        flags |= os.O_DIRECTORY
    else:
        flags |= getattr(os, "O_NONBLOCK", 0)
    return flags


def _open_parent(
    workspace: Path,
    relative_path: str,
    *,
    create_parents: bool,
) -> tuple[list[int], int, str]:
    """Open a path's parent through retained directory descriptors."""

    root = _workspace_root(workspace)
    relative = PurePosixPath(canonical_relative_path(relative_path))
    descriptors: list[int] = []
    try:
        current = os.open(root, _open_flags(directory=True))
        descriptors.append(current)
        for component in relative.parts[:-1]:
            if create_parents:
                try:
                    os.mkdir(component, mode=0o700, dir_fd=current)
                    os.fsync(current)
                except FileExistsError:
                    pass
            current = os.open(component, _open_flags(directory=True), dir_fd=current)
            descriptors.append(current)
        return descriptors, current, relative.parts[-1]
    except OSError as exc:
        for descriptor in reversed(descriptors):
            os.close(descriptor)
        raise CausalMaterializerIOError(
            f"cannot open evidence parent safely: {relative_path}"
        ) from exc


def safe_read(
    workspace: Path,
    relative_path: str,
    *,
    max_bytes: int,
    expected_sha256: str | None = None,
    expected_size: int | None = None,
) -> bytes:
    """Read one bounded single-link regular file from one stable descriptor."""

    if max_bytes < 1:
        raise CausalMaterializerIOError("read ceiling must be positive")
    descriptors, parent, leaf = _open_parent(
        workspace, relative_path, create_parents=False
    )
    try:
        descriptor = os.open(leaf, _open_flags(directory=False), dir_fd=parent)
        descriptors.append(descriptor)
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise CausalMaterializerIOError(
                "evidence leaf must be one singly linked regular file"
            )
        if before.st_size < 1 or before.st_size > max_bytes:
            raise CausalMaterializerIOError("evidence file exceeds its fixed byte ceiling")
        if expected_size is not None and before.st_size != expected_size:
            raise CausalMaterializerIOError("evidence size differs from its descriptor")
        remaining = before.st_size
        chunks: list[bytes] = []
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                raise CausalMaterializerIOError("evidence file shortened during read")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise CausalMaterializerIOError("evidence file grew during read")
        after = os.fstat(descriptor)
        if (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ):
            raise CausalMaterializerIOError("evidence metadata changed during read")
        data = b"".join(chunks)
        if expected_sha256 is not None and tagged_sha256(data) != expected_sha256:
            raise CausalMaterializerIOError("evidence digest differs from its descriptor")
        return data
    except OSError as exc:
        raise CausalMaterializerIOError(
            f"cannot reopen evidence safely: {relative_path}"
        ) from exc
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def write_create_only(
    workspace: Path,
    relative_path: str,
    data: bytes,
    *,
    max_bytes: int,
) -> None:
    """Publish one immutable file or accept a byte-identical idempotent retry."""

    if not isinstance(data, bytes) or not data or len(data) > max_bytes:
        raise CausalMaterializerIOError("create-only evidence violates its byte ceiling")
    descriptors, parent, leaf = _open_parent(
        workspace, relative_path, create_parents=True
    )
    temporary = f".{leaf}.{secrets.token_hex(12)}.tmp"
    created_temporary = False
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW
        descriptor = os.open(temporary, flags, 0o600, dir_fd=parent)
        created_temporary = True
        try:
            view = memoryview(data)
            while view:
                written = os.write(descriptor, view)
                if written <= 0:
                    raise CausalMaterializerIOError("short write to immutable evidence")
                view = view[written:]
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        try:
            os.link(
                temporary,
                leaf,
                src_dir_fd=parent,
                dst_dir_fd=parent,
                follow_symlinks=False,
            )
            os.fsync(parent)
        except FileExistsError:
            existing = safe_read(
                workspace,
                relative_path,
                max_bytes=max_bytes,
                expected_sha256=tagged_sha256(data),
                expected_size=len(data),
            )
            if existing != data:
                raise CausalMaterializerIOError(
                    f"immutable evidence collision at {relative_path}"
                )
    except OSError as exc:
        raise CausalMaterializerIOError(
            f"cannot create immutable evidence safely: {relative_path}"
        ) from exc
    finally:
        if created_temporary:
            try:
                os.unlink(temporary, dir_fd=parent)
            except FileNotFoundError:
                pass
        for directory in reversed(descriptors):
            os.close(directory)


def evidence_ref(
    *,
    path: str,
    data: bytes,
    namespace: Mapping[str, Any],
) -> dict[str, Any]:
    """Describe exact bytes without embedding them in higher-level evidence."""

    return {
        "path": canonical_relative_path(path),
        "sha256": tagged_sha256(data),
        "size_bytes": len(data),
        "namespace": dict(namespace),
        "media_type": JSON_MEDIA_TYPE,
    }


def read_ref(workspace: Path, ref: Mapping[str, Any], *, max_bytes: int) -> bytes:
    """Reopen one exact compact reference under a fixed caller-selected ceiling."""

    required = {"path", "sha256", "size_bytes", "namespace", "media_type"}
    if set(ref) != required or ref.get("media_type") != JSON_MEDIA_TYPE:
        raise CausalMaterializerIOError("compact evidence reference is not closed")
    size = ref.get("size_bytes")
    if isinstance(size, bool) or not isinstance(size, int) or size < 1 or size > max_bytes:
        raise CausalMaterializerIOError("compact evidence size is invalid")
    return safe_read(
        workspace,
        str(ref.get("path", "")),
        max_bytes=max_bytes,
        expected_sha256=str(ref.get("sha256", "")),
        expected_size=size,
    )


def decode_canonical_object(data: bytes, *, label: str) -> dict[str, Any]:
    """Decode one canonical JSON object, rejecting alternate byte encodings."""

    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CausalMaterializerIOError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json_bytes(value) != data:
        raise CausalMaterializerIOError(f"{label} is not one canonical JSON object")
    return value


def read_bounded_stdin(*, max_bytes: int, label: str) -> dict[str, Any]:
    """Read one bounded canonical protocol object from standard input."""

    chunks: list[bytes] = []
    total = 0
    while total <= max_bytes:
        chunk = os.read(0, min(64 * 1024, max_bytes + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
    data = b"".join(chunks)
    if not data or len(data) > max_bytes:
        raise CausalMaterializerIOError(f"{label} exceeds its fixed input ceiling")
    return decode_canonical_object(data, label=label)


__all__ = [
    "CausalMaterializerIOError",
    "JSON_MEDIA_TYPE",
    "MAX_ARTIFACT_BYTES",
    "MAX_ATTEMPTS",
    "MAX_BINDING_BYTES",
    "MAX_PATH_BYTES",
    "MAX_RECEIPT_BYTES",
    "MAX_REQUEST_BYTES",
    "SUBPROCESS_TIMEOUT_SECONDS",
    "canonical_json_bytes",
    "canonical_relative_path",
    "decode_canonical_object",
    "evidence_ref",
    "read_bounded_stdin",
    "read_ref",
    "safe_read",
    "tagged_sha256",
    "write_create_only",
]
