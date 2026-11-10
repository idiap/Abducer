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
"""Centralized inert-text formatting for public reasoning-trace LaTeX."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import PurePosixPath
from typing import Any


class UnsafePublicValue(ValueError):
    """A value cannot safely appear in a public trace."""


SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.I),
    re.compile(r"\b(?:sk|ghp|glpat)-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\b(?:api[_-]?key|password|secret)\s*[:=]\s*\S+", re.I),
)
ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9_.-])/(?:Users|home|root|private|etc|var|opt|tmp)/[^\s,;]+")

_TEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "%": r"\%",
    "_": r"\_",
    "^": r"\textasciicircum{}",
    "~": r"\textasciitilde{}",
}


def redact_public_text(value: str) -> str:
    """Redact secrets and host-local absolute paths before TeX processing."""
    normalized = unicodedata.normalize("NFC", value)
    for pattern in SECRET_PATTERNS:
        normalized = pattern.sub("[REDACTED SECRET]", normalized)
    normalized = ABSOLUTE_PATH.sub("[REDACTED ABSOLUTE LOCAL PATH]", normalized)
    return normalized


def normalize_public_path(value: str) -> str:
    """Accept repository-relative references and visibly redact local absolutes."""
    value = redact_public_text(value.strip().replace("\\", "/"))
    if value.startswith("/") or re.match(r"^[A-Za-z]:/", value):
        return "[REDACTED ABSOLUTE LOCAL PATH]"
    path = PurePosixPath(value)
    if ".." in path.parts:
        raise UnsafePublicValue("parent traversal is not a public artifact reference")
    return str(path)


def _strip_controls(value: str) -> str:
    result = []
    for char in value:
        category = unicodedata.category(char)
        if char in "\n\t":
            result.append(" " if char == "\t" else "\n")
        elif category not in {"Cc", "Cf", "Cs", "Co", "Cn"}:
            result.append(char)
        else:
            result.append("�")
    return "".join(result)


def tex_escape(value: Any) -> str:
    """Render a packet-derived scalar as inert text, never as trusted TeX."""
    if value is None:
        text = ""
    elif isinstance(value, bool):
        text = "true" if value else "false"
    elif isinstance(value, (dict, list, tuple)):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(", ", ": "))
    else:
        text = str(value)
    text = _strip_controls(redact_public_text(text))
    return "".join(_TEX_ESCAPES.get(char, char) for char in text)


def safe_text(value: Any) -> str:
    """Compatibility name for the sole packet-to-TeX text boundary."""
    return tex_escape(value)


def wrap_long_tex_token(escaped: str, width: int = 10) -> str:
    """Add renderer-owned break opportunities without interpreting input."""
    if width < 8:
        raise ValueError("wrap width must be at least 8")
    chunks: list[str] = []
    count = 0
    index = 0
    while index < len(escaped):
        # Keep generated control sequences intact.
        if escaped[index] == "\\":
            match = re.match(r"\\(?:[A-Za-z]+(?:\{\})?|.)", escaped[index:])
            token = match.group(0) if match else escaped[index]
        else:
            token = escaped[index]
        chunks.append(token)
        index += len(token)
        if token.isspace():
            count = 0
        else:
            count += 1
        if token in {"/", ".", ":", "-", r"\_"} or count >= width:
            chunks.append(r"\allowbreak{}")
            count = 0
    return "".join(chunks)


def format_value(value: Any, *, wrap: bool = True) -> str:
    escaped = tex_escape(value)
    return wrap_long_tex_token(escaped) if wrap else escaped


def assert_no_unsafe_public_values(value: Any, path: str = "packet") -> None:
    """Strict opt-in validator used before release compilation.

    Rendering itself redacts to remain non-destructive; callers that need a
    hard failure can invoke this traversal before producing artifacts.
    """
    if isinstance(value, dict):
        for key, child in value.items():
            assert_no_unsafe_public_values(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_unsafe_public_values(child, f"{path}[{index}]")
    elif isinstance(value, str):
        if any(pattern.search(value) for pattern in SECRET_PATTERNS):
            raise UnsafePublicValue(f"secret-like value at {path}")
        if ABSOLUTE_PATH.search(value) or value.startswith("/"):
            raise UnsafePublicValue(f"absolute local path at {path}")
