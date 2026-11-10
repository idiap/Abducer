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
"""Derive Route A endpoint incidence weights from validated path channels."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


def endpoints(channel: dict[str, Any]) -> list[tuple[float, ...]]:
    edges = channel.get("edges", [])
    verts = []
    for e in edges:
        verts.extend([tuple(float(x) for x in e[0]), tuple(float(x) for x in e[1])])
    if not verts:
        return []
    counts: dict[tuple[float, ...], int] = {}
    for v in verts:
        counts[v] = counts.get(v, 0) + 1
    return sorted([v for v, count in counts.items() if count == 1]) or [verts[0], verts[-1]]


def derive(data: dict[str, Any], null_vector: list[float]) -> dict[str, Any]:
    channels = data.get("channels", [])
    names = [c.get("name", f"ch{i}") for i, c in enumerate(channels)]
    if len(names) != len(null_vector):
        raise ValueError("null vector length must match channel count")
    boxes = {name: endpoints(channel) for name, channel in zip(names, channels)}
    pair_weights = {}
    for (i, ni), (j, nj) in combinations(enumerate(names), 2):
        pair_weights[f"{ni},{nj}"] = 2 * null_vector[i] * null_vector[j]
    diagonal_weights = {name: null_vector[i] ** 2 for i, name in enumerate(names)}
    zero_diagonal_required = any(abs(v) > 1e-12 for v in diagonal_weights.values())
    return {
        "schema": "abducer.routea_endpoint_incidence.v1",
        "candidate_id": data.get("candidate_id", "unknown"),
        "channels": names,
        "endpoint_boxes": {k: [list(v) for v in vals] for k, vals in boxes.items()},
        "null_vector": null_vector,
        "diagonal_weights": diagonal_weights,
        "zero_diagonal_required_for_offdiag_reduction": zero_diagonal_required,
        "offdiagonal_pair_weights": pair_weights,
        "color_convention": "SU(2) normalized trace and singlet projection must be supplied before local integral promotion",
        "sign_claim_boundary": "incidence weights alone do not determine endpoint sign",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--null-vector", default="1,1,-2")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.candidate.read_text(encoding="utf-8"))
    null_vector = [float(x) for x in args.null_vector.split(",")]
    report = derive(data, null_vector)
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
