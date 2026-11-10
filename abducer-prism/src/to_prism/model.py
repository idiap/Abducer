# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Shared model vocabulary and invariant helpers."""

from __future__ import annotations

from enum import StrEnum

SCHEMA_VERSION = "1.0"


class ReviewStatus(StrEnum):
    EXTRACTED = "extracted"
    PROPOSED = "proposed"
    REVIEWED = "reviewed"
    APPROVED = "approved"


class Disposition(StrEnum):
    CONVERT = "convert"
    WRAP = "wrap"
    COPY = "copy"
    EXCLUDE = "exclude"
    UNSUPPORTED = "unsupported"
    UNRESOLVED = "unresolved"


class PreservationStatus(StrEnum):
    ESTABLISHED = "established"
    NOT_APPLICABLE = "not_applicable"
    NOT_TESTED = "not_tested"
    UNSUPPORTED = "unsupported"
    FAILED = "failed"


PRESERVATION_LEVELS = (
    "asset",
    "structural",
    "contract",
    "trace",
    "behavioral",
    "epistemic",
)


def require_unique(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise ValueError(f"duplicate {label}: {', '.join(duplicates)}")
