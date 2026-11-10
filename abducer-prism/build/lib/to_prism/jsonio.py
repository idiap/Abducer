"""Canonical JSON and content hashing helpers."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> str:
    """Return stable UTF-8 JSON text with a single trailing newline."""

    return (
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        )
        + "\n"
    )


def canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def document_hash(value: Any) -> str:
    return f"sha256:{sha256_bytes(canonical_bytes(value))}"


def read_json(path: str | os.PathLike[str]) -> Any:
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path: str | os.PathLike[str], value: Any) -> None:
    """Write canonical JSON atomically without following a final symlink."""

    write_text(path, canonical_json(value))


def write_text(path: str | os.PathLike[str], value: str) -> None:
    """Write text atomically without following a final symlink."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        raise ValueError(f"refusing to replace symlink: {target}")
    temporary = target.with_name(f".{target.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)
