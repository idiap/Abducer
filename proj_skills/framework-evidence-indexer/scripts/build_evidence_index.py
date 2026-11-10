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
"""Build a deterministic, bounded repository evidence index without executing inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

PARSER_VERSION = "framework-evidence-indexer/1.0.0"
DEFAULT_SUFFIXES = (".json", ".md", ".py", ".tex", ".toml", ".yaml", ".yml")
DEFAULT_EXCLUDED = (
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".venv-pmp",
    "__pycache__",
    "agentic/reports",
    "artifacts",
    "artifacts/project-papers",
    "external",
    "node_modules",
    "private",
    "vendor",
)
SECRET_NAMES = {".env", ".env.local", "id_dsa", "id_ed25519", "id_rsa", "secrets.json"}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}"),
)


class IndexingError(RuntimeError):
    """Raised when bounded evidence intake cannot safely continue."""


@dataclass(frozen=True)
class Policy:
    max_files: int
    max_file_bytes: int
    max_total_bytes: int
    allowed_suffixes: tuple[str, ...]
    excluded_components: tuple[str, ...]


def _digest(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _component_excluded(relative: PurePosixPath, exclusions: tuple[str, ...]) -> bool:
    text = relative.as_posix()
    for raw in exclusions:
        item = PurePosixPath(raw.strip("/"))
        if len(item.parts) == 1 and item.parts[0] in relative.parts:
            return True
        if text == item.as_posix() or text.startswith(f"{item.as_posix()}/"):
            return True
    return False


def _walk(root: Path, policy: Policy) -> Iterable[tuple[Path, PurePosixPath]]:
    stack: list[tuple[Path, PurePosixPath]] = [(root, PurePosixPath("."))]
    while stack:
        directory, relative_dir = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name, reverse=True)
        except OSError as exc:
            raise IndexingError(f"cannot scan {relative_dir.as_posix()}: {exc}") from exc
        for entry in entries:
            relative = PurePosixPath(entry.name) if relative_dir == PurePosixPath(".") else relative_dir / entry.name
            if _component_excluded(relative, policy.excluded_components):
                continue
            if entry.is_symlink():
                raise IndexingError(f"symlink is not eligible evidence: {relative.as_posix()}")
            if entry.is_dir(follow_symlinks=False):
                stack.append((Path(entry.path), relative))
            elif entry.is_file(follow_symlinks=False):
                if entry.name.lower() in SECRET_NAMES:
                    raise IndexingError(f"suspected secret file is not eligible evidence: {relative.as_posix()}")
                if Path(entry.name).suffix.lower() in policy.allowed_suffixes:
                    yield Path(entry.path), relative


def _classify(path: PurePosixPath) -> tuple[str, str, str]:
    text = path.as_posix()
    parts = set(path.parts)
    name = path.name.lower()
    if "tests" in parts or name.startswith("test_"):
        return "test", "verification", "observed"
    if text.startswith("agentic/spec/") or "registries" in parts or name in {"agents.md", "pyproject.toml"}:
        return "contract", "normative", "declared"
    if path.suffix == ".py":
        return "implementation", "implementation", "observed"
    if "receipts" in parts or "evals" in parts:
        return "execution_receipt", "verification", "unknown"
    if "artifacts" in parts:
        return "artifact", "derived", "unknown"
    if text.startswith("docs/") or path.suffix == ".tex" or name in {"readme.md", "skill.md"}:
        return "documentation", "explanatory", "declared"
    if "history" in parts:
        return "history", "historical", "unknown"
    return "interpretation", "derived", "unknown"


def _git_state(root: Path) -> dict[str, object]:
    def run(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )

    try:
        inside = run("rev-parse", "--is-inside-work-tree")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {"revision": None, "git_available": False, "dirty": None}
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return {"revision": None, "git_available": False, "dirty": None}
    revision = run("rev-parse", "HEAD")
    status = run("status", "--porcelain", "--untracked-files=normal")
    return {
        "revision": revision.stdout.strip() if revision.returncode == 0 else None,
        "git_available": True,
        "dirty": bool(status.stdout.strip()) if status.returncode == 0 else None,
    }


def build_index(root: Path, policy: Policy) -> dict[str, object]:
    root = root.resolve()
    if not root.is_dir():
        raise IndexingError("repository root must be an existing directory")
    records: list[dict[str, object]] = []
    total_bytes = 0
    for absolute, relative in _walk(root, policy):
        relative_text = relative.as_posix()
        if relative.name.lower() in SECRET_NAMES:
            raise IndexingError(f"suspected secret file is not eligible evidence: {relative_text}")
        try:
            size = absolute.stat(follow_symlinks=False).st_size
        except OSError as exc:
            raise IndexingError(f"cannot stat {relative_text}: {exc}") from exc
        if size > policy.max_file_bytes:
            raise IndexingError(f"eligible file exceeds max_file_bytes: {relative_text}")
        total_bytes += size
        if total_bytes > policy.max_total_bytes:
            raise IndexingError("eligible inputs exceed max_total_bytes")
        if len(records) >= policy.max_files:
            raise IndexingError("eligible inputs exceed max_files")
        data = absolute.read_bytes()
        if any(pattern.search(data) for pattern in SECRET_PATTERNS):
            raise IndexingError(f"suspected secret content in eligible file: {relative_text}")
        content_digest = _digest(data)
        kind, authority, posture = _classify(relative)
        records.append(
            {
                "evidence_id": f"EV-{content_digest.removeprefix('sha256:')[:16]}",
                "path": relative_text,
                "kind": kind,
                "authority": authority,
                "posture": posture,
                "digest": content_digest,
                "bytes": size,
                "freshness": "current",
            }
        )
    records.sort(key=lambda record: str(record["path"]))
    payload: dict[str, object] = {
        "schema_version": "1.0.0",
        "parser_version": PARSER_VERSION,
        "repository": _git_state(root),
        "source_policy": {
            "max_files": policy.max_files,
            "max_file_bytes": policy.max_file_bytes,
            "max_total_bytes": policy.max_total_bytes,
            "allowed_suffixes": list(policy.allowed_suffixes),
            "excluded_components": list(policy.excluded_components),
        },
        "records": records,
        "conflicts": [],
        "warnings": [],
    }
    payload["index_digest"] = _digest(_canonical_bytes(payload))
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-files", type=int, default=10_000)
    parser.add_argument("--max-file-bytes", type=int, default=2_000_000)
    parser.add_argument("--max-total-bytes", type=int, default=100_000_000)
    parser.add_argument("--suffix", action="append", dest="suffixes")
    args = parser.parse_args(argv)
    suffixes = tuple(sorted(set(args.suffixes or DEFAULT_SUFFIXES)))
    if any(not suffix.startswith(".") for suffix in suffixes):
        parser.error("every --suffix must start with '.'")
    if min(args.max_files, args.max_file_bytes, args.max_total_bytes) < 1:
        parser.error("all bounds must be positive")
    policy = Policy(args.max_files, args.max_file_bytes, args.max_total_bytes, suffixes, DEFAULT_EXCLUDED)
    try:
        index = build_index(args.repo, policy)
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (IndexingError, OSError) as exc:
        print(f"evidence indexing failed: {exc}", file=sys.stderr)
        return 2
    print(f"indexed {len(index['records'])} files -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
