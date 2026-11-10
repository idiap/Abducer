# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Read-only descriptors for established specialized report projections."""

from __future__ import annotations

from typing import Any


SUPPORTED = {"process_graph", "reasoning_dynamics", "conceptual_dynamics", "yang_mills_monitor"}


def adapt_legacy_projection(kind: str, payload: dict[str, Any], source_path: str) -> dict[str, Any]:
    """Describe a legacy input without interpreting it as scientific inference.

    The existing generator remains authoritative for its report.  The generic
    trace may link to this descriptor, but it never rewrites the source packet
    or promotes a successful legacy status into a public claim.
    """

    if kind not in SUPPORTED:
        raise ValueError(f"unsupported legacy projection: {kind}")
    if source_path.startswith("/") or ".." in source_path.split("/"):
        raise ValueError("legacy source_path must be repository-relative")
    version = payload.get("version") or payload.get("schema_version") or "unknown"
    return {
        "projection_kind": kind,
        "source_path": source_path,
        "source_version": version,
        "read_only": True,
        "public_inference_status": "trace_incomplete",
        "compatibility_note": "Rendered by the established specialized generator; no scientific rationale inferred by the generic adapter.",
    }
