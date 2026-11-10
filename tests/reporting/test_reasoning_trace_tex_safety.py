# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))
from reasoning_trace_tex_safety import (  # noqa: E402
    UnsafePublicValue, assert_no_unsafe_public_values, format_value, normalize_public_path, tex_escape,
)


def test_all_tex_metacharacters_are_inert() -> None:
    value = r"\input{/etc/passwd} \include{x} \write18{touch pwn} $x & y # z % q _ ^ ~ { }"
    escaped = tex_escape(value)
    assert r"\textbackslash{}input" in escaped
    assert r"\textbackslash{}write" in escaped
    assert r"\$" in escaped and r"\&" in escaped and r"\#" in escaped and r"\%" in escaped
    assert r"\_" in escaped and r"\textasciicircum{}" in escaped and r"\textasciitilde{}" in escaped
    assert r"\input{" not in escaped and r"\write18{" not in escaped


def test_unicode_controls_secrets_and_absolute_paths_are_handled() -> None:
    escaped = tex_escape("café α\x00 sk-abcdefghijklmnopqrstuvwxyz /Users/alice/private.txt")
    assert "café α�" in escaped
    assert "REDACTED SECRET" in escaped
    assert "REDACTED ABSOLUTE LOCAL PATH" in escaped
    with pytest.raises(UnsafePublicValue):
        assert_no_unsafe_public_values({"token": "sk-abcdefghijklmnopqrstuvwxyz"})
    with pytest.raises(UnsafePublicValue):
        assert_no_unsafe_public_values({"path": "/Users/alice/private.txt"})


def test_repository_paths_and_long_identifiers_remain_traceable() -> None:
    assert normalize_public_path("tests/fixtures/evidence.json") == "tests/fixtures/evidence.json"
    with pytest.raises(UnsafePublicValue):
        normalize_public_path("../../secret")
    rendered = format_value("x" * 150)
    assert rendered.count(r"\allowbreak{}") >= 3

