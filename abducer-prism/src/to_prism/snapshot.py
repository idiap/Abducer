# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Allowlisted source snapshots for portable converted projects."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

_PROTECTED = re.compile(
    r"(?i)(^|/)(\.env($|\.)|credentials?|secrets?|id_(rsa|dsa|ecdsa|ed25519)|.*\.(pem|p12|pfx|key)$)"
)


def create_allowlisted_snapshot(
    *, source_root: Path, project_root: Path, entries: list[dict[str, Any]]
) -> tuple[dict[str, Any], ...]:
    """Copy only reviewed files, retaining relative paths and license decisions."""
    root = source_root.resolve()
    destination = project_root / "source_snapshot"
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for specification in entries:
        relative = Path(str(specification.get("path", "")))
        normalized = relative.as_posix()
        if (
            not normalized
            or relative.is_absolute()
            or ".." in relative.parts
            or normalized in seen
        ):
            raise ValueError(f"snapshot path is invalid or duplicated: {normalized!r}")
        if _PROTECTED.search(normalized):
            raise ValueError(
                f"credential-shaped snapshot path is prohibited: {normalized}"
            )
        license_disposition = str(specification.get("license", "")).strip()
        if not license_disposition:
            raise ValueError(
                f"snapshot path lacks a reviewed license disposition: {normalized}"
            )
        candidate = root / relative
        source = candidate.resolve()
        if root not in source.parents or candidate.is_symlink() or not source.is_file():
            raise ValueError(
                f"snapshot source must be a regular in-scope file: {normalized}"
            )
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        records.append(
            {
                "license": license_disposition,
                "path": normalized,
                "purpose": str(specification.get("purpose", "runtime-leaf")),
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            }
        )
        seen.add(normalized)
    ordered = tuple(sorted(records, key=lambda item: item["path"]))
    if ordered:
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "manifest.json").write_text(
            json.dumps(ordered, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return ordered


__all__ = ["create_allowlisted_snapshot"]
