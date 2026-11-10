"""Path containment, staging, and publication safety."""

from __future__ import annotations

import os
import shutil
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterator


class PathSafetyError(ValueError):
    """Raised when source/output separation cannot be established."""


def canonical_path(path: str | os.PathLike[str], *, must_exist: bool = False) -> Path:
    candidate = Path(path).expanduser()
    try:
        return candidate.resolve(strict=must_exist)
    except (OSError, RuntimeError) as exc:
        raise PathSafetyError(f"cannot resolve path {candidate!s}: {exc}") from exc


def is_within(path: str | os.PathLike[str], root: str | os.PathLike[str]) -> bool:
    resolved_path = canonical_path(path)
    resolved_root = canonical_path(root)
    return resolved_path == resolved_root or resolved_root in resolved_path.parents


def normalize_relative_path(path: str | os.PathLike[str]) -> str:
    """Normalize an artifact path and reject absolute/escaping spellings."""

    text = os.fspath(path).replace("\\", "/")
    pure = PurePosixPath(text)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise PathSafetyError(f"path must be a normalized relative path: {text!r}")
    return pure.as_posix()


def resolve_member(
    root: str | os.PathLike[str],
    relative: str | os.PathLike[str],
    *,
    must_exist: bool = False,
) -> Path:
    base = canonical_path(root, must_exist=True)
    normalized = normalize_relative_path(relative)
    member = canonical_path(base / normalized, must_exist=must_exist)
    if member != base and base not in member.parents:
        raise PathSafetyError(f"path escapes declared root: {normalized}")
    return member


def ensure_disjoint(
    source: str | os.PathLike[str], output: str | os.PathLike[str]
) -> tuple[Path, Path]:
    source_path = canonical_path(source, must_exist=True)
    raw_output = Path(output).expanduser()
    if raw_output.is_symlink():
        raise PathSafetyError("output root must not be a symlink")
    if not source_path.is_dir():
        raise PathSafetyError("source must be an existing directory")
    output_path = canonical_path(output)
    if source_path == output_path:
        raise PathSafetyError("source and output resolve to the same directory")
    if source_path in output_path.parents:
        raise PathSafetyError("output must not be inside source")
    if output_path in source_path.parents:
        raise PathSafetyError("source must not be inside output")
    return source_path, output_path


@dataclass(frozen=True, slots=True)
class ConversionPaths:
    source: Path
    output: Path

    @classmethod
    def resolve(
        cls, source: str | os.PathLike[str], output: str | os.PathLike[str]
    ) -> "ConversionPaths":
        resolved_source, resolved_output = ensure_disjoint(source, output)
        return cls(source=resolved_source, output=resolved_output)


@contextmanager
def staging_directory(output: str | os.PathLike[str]) -> Iterator[Path]:
    """Create a same-filesystem sibling stage which is removed on failure."""

    destination = canonical_path(output)
    parent = destination.parent
    parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{destination.name}.stage-", dir=parent))
    try:
        yield stage
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def publish_directory(
    stage: str | os.PathLike[str],
    output: str | os.PathLike[str],
    *,
    replace: bool = False,
) -> None:
    """Atomically publish a completed sibling stage, rolling back replacement."""

    staged = canonical_path(stage, must_exist=True)
    destination = canonical_path(output)
    if staged.parent != destination.parent:
        raise PathSafetyError("stage and output must share a parent filesystem")
    if destination.exists() and not replace:
        raise FileExistsError(f"output already exists: {destination}")
    backup = destination.with_name(f".{destination.name}.previous-{os.getpid()}")
    if backup.exists():
        raise FileExistsError(f"publication backup already exists: {backup}")
    moved_old = False
    try:
        if destination.exists():
            os.replace(destination, backup)
            moved_old = True
        os.replace(staged, destination)
    except BaseException:
        if moved_old and backup.exists() and not destination.exists():
            os.replace(backup, destination)
        raise
    else:
        if backup.exists():
            shutil.rmtree(backup)


# Compatibility names kept intentionally small and explicit.
path_within = is_within
resolve_paths = ConversionPaths.resolve
