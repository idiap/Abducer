# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Deterministic identifiers for solver artifacts.

Every artifact (concept, task, failure, candidate, edge, ...) gets an id derived purely
from its own content via `stable_id`, never from a counter or random UUID. That means
re-running the same input always produces the same ids, which is what lets the run ledger
resume a partial run and lets tests assert on exact id values.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


def slugify(value: str) -> str:
    """Turn arbitrary text into a lowercase, hyphenated id-safe fragment."""

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "artifact"


def stable_hash(payload: Any, length: int = 10) -> str:
    """Hash any JSON-serializable payload to a short, content-derived hex digest."""

    rendered = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()[:length]


def stable_id(prefix: str, payload: Any) -> str:
    """Build a `<prefix>_<readable-slug>_<content-hash>` id for a payload.

    The slug (from the payload's own id/name/label, if any) keeps ids human-scannable in
    logs and reports; the trailing hash keeps them unique and content-addressed so two
    semantically different payloads never collide even if their labels match.
    """

    label = ""
    if isinstance(payload, dict):
        label = str(payload.get("id") or payload.get("name") or payload.get("label") or "")
    elif hasattr(payload, "id"):
        label = str(getattr(payload, "id"))
    elif hasattr(payload, "name"):
        label = str(getattr(payload, "name"))
    base = slugify(label) if label else prefix
    return f"{prefix}_{base}_{stable_hash(payload)}"
