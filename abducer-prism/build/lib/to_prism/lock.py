"""Stable conversion lock construction and ownership checks."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path
from typing import Any, Iterable

from . import __version__
from .jsonio import document_hash
from .model import SCHEMA_VERSION
from .paths import canonical_path, normalize_relative_path


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def generated_file_records(
    project_root: str | os.PathLike[str], relative_paths: Iterable[str]
) -> list[dict[str, Any]]:
    root = canonical_path(project_root, must_exist=True)
    records = []
    for relative in sorted(set(relative_paths)):
        normalized = normalize_relative_path(relative)
        path = root / normalized
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise ValueError(f"generated path must be a regular file: {normalized}")
        records.append(
            {
                "content_hash": _hash_file(path),
                "executable": bool(metadata.st_mode & 0o111),
                "owner": "generator",
                "path": normalized,
            }
        )
    return records


def build_lock(
    *,
    inventory: dict[str, Any],
    decisions: dict[str, Any],
    generated_files: list[dict[str, Any]],
    profile_versions: dict[str, str],
    prism: dict[str, Any],
    template_version: str,
) -> dict[str, Any]:
    return {
        "artifact": "to-prism-lock",
        "converter_version": __version__,
        "decisions_hash": document_hash(decisions),
        "generated_files": sorted(generated_files, key=lambda item: item["path"]),
        "inventory_hash": document_hash(inventory),
        "prism": prism,
        "profile_versions": dict(sorted(profile_versions.items())),
        "schema_version": SCHEMA_VERSION,
        "source_fingerprint": inventory["source"]["fingerprint"],
        "template_version": template_version,
    }


def verify_generated_ownership(
    output_root: str | os.PathLike[str], lock_document: dict[str, Any]
) -> list[dict[str, str]]:
    root = canonical_path(output_root, must_exist=True)
    changes: list[dict[str, str]] = []
    for record in lock_document.get("generated_files", []):
        relative = normalize_relative_path(record["path"])
        path = root / relative
        if not path.exists() or path.is_symlink() or not path.is_file():
            changes.append({"path": relative, "status": "missing-or-wrong-type"})
            continue
        if _hash_file(path) != record["content_hash"]:
            changes.append({"path": relative, "status": "modified"})
        elif bool(path.stat().st_mode & 0o111) != bool(record.get("executable", False)):
            changes.append({"path": relative, "status": "mode-changed"})
    return changes


def require_supported_lock(lock_document: dict[str, Any]) -> None:
    if lock_document.get("artifact") != "to-prism-lock":
        raise ValueError("not a to-prism lock document")
    if lock_document.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"unsupported lock schema version: {lock_document.get('schema_version')!r}"
        )
