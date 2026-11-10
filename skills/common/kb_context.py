# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Utilities for resolving canonical KB references and artifact roots."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


_KB_REF_RE = re.compile(r"[^a-z0-9-]+")


def normalize_kb_ref(raw: str) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Produces canonical KB reference IDs so artifact routing remains deterministic.
    """

    text = str(raw or "").strip().lower()
    if not text:
        return ""
    text = text.replace("_", "-").replace(" ", "-")
    text = _KB_REF_RE.sub("-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text


def kb_ref_from_kb_filename(kb_path: Path) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Typed classification used to guide routing and filtering.
    Contribution: Maps KB filenames to stable reference IDs used by downstream stages.
    """

    name = kb_path.name
    if name.endswith(".kb.md"):
        return normalize_kb_ref(name[: -len(".kb.md")])
    return normalize_kb_ref(kb_path.stem)


def read_front_matter_kb_id(kb_path: Path) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Reads KB identity from front matter when available.
    """

    try:
        text = kb_path.read_text(encoding="utf-8")
    except OSError:
        return ""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:]:
        s = line.strip()
        if s == "---":
            break
        if not s or s.startswith("#"):
            continue
        if ":" not in s:
            continue
        key, value = s.split(":", 1)
        if key.strip() == "kb_id":
            return normalize_kb_ref(value.strip().strip("'\""))
    return ""


def resolve_kb_reference(kb_path: Path, explicit_kb_ref: str = "") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Resolves a single canonical KB reference and rejects inconsistent identities.
    """

    filename_ref = kb_ref_from_kb_filename(kb_path)
    fm_ref = read_front_matter_kb_id(kb_path) if kb_path.exists() else ""
    explicit_ref = normalize_kb_ref(explicit_kb_ref)

    chosen = explicit_ref or fm_ref or filename_ref
    if not chosen:
        raise ValueError(f"Unable to resolve KB reference for path: {kb_path}")
    if explicit_ref and fm_ref and explicit_ref != fm_ref:
        raise ValueError(f"Explicit --kb-ref `{explicit_ref}` does not match KB front matter kb_id `{fm_ref}`.")
    return {
        "kb_ref": chosen,
        "kb_ref_from_filename": filename_ref,
        "kb_ref_from_front_matter": fm_ref,
    }


def canonical_artifacts_dir(repo_root: Path, kb_ref: str) -> Path:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Produces canonical per-KB artifact directories.
    """

    return (repo_root / "artifacts" / normalize_kb_ref(kb_ref)).resolve()


def kb_ref_from_artifacts_dir(artifacts_dir: Path) -> str:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Typed classification used to guide routing and filtering.
    Contribution: Recovers KB reference from artifacts directory naming convention.
    """

    return normalize_kb_ref(artifacts_dir.name)
