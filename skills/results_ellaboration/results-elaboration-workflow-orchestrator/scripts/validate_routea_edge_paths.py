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
"""Validate explicit Route A collar path candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def vertex(v: Any) -> tuple[float, float, float, float]:
    if not isinstance(v, list) or len(v) != 4:
        raise ValueError(f"vertex must be a length-4 list, got {v!r}")
    return tuple(float(x) for x in v)  # type: ignore[return-value]


def edge(e: Any) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
    if not isinstance(e, list) or len(e) != 2:
        raise ValueError(f"edge must be [source,target], got {e!r}")
    return vertex(e[0]), vertex(e[1])


def canonical_edge(e: Any) -> tuple[tuple[float, ...], tuple[float, ...]]:
    a, b = edge(e)
    return a, b


def canonical_path(edges: list[Any]) -> list[tuple[tuple[float, ...], tuple[float, ...]]]:
    return [canonical_edge(e) for e in edges]


def reflect_vertex(v: tuple[float, ...], reflection: dict[str, Any]) -> tuple[float, ...]:
    axis = int(reflection.get("axis", 2))
    offset = float(reflection.get("offset", 0.0))
    out = list(v)
    out[axis] = 2 * offset - out[axis]
    return tuple(out)


def reflect_edge(
    e: tuple[tuple[float, ...], tuple[float, ...]], reflection: dict[str, Any]
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    return reflect_vertex(e[0], reflection), reflect_vertex(e[1], reflection)


def same_edge(a: tuple[tuple[float, ...], tuple[float, ...]], b: tuple[tuple[float, ...], tuple[float, ...]]) -> bool:
    return a == b or a == (b[1], b[0])


def path_vertices(path: list[tuple[tuple[float, ...], tuple[float, ...]]]) -> list[tuple[float, ...]]:
    verts: list[tuple[float, ...]] = []
    for a, b in path:
        if not verts:
            verts.append(a)
        verts.append(b)
    return verts


def validate(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    positive_time_min = float(data.get("positive_time_min", 1))
    reflection = data.get("reflection", {"axis": 2, "offset": 0})
    channels = {c["name"]: c for c in data.get("channels", [])}
    paths = {name: canonical_path(c.get("edges", [])) for name, c in channels.items()}

    if not channels:
        errors.append("no channels supplied")

    for name, path in paths.items():
        if not path:
            errors.append(f"channel {name} has no edges")
        for idx, (a, b) in enumerate(path):
            if a[0] < positive_time_min or b[0] < positive_time_min:
                errors.append(f"channel {name} edge {idx} leaves positive-time support: {a}->{b}")

    for name, channel in channels.items():
        partner = channel.get("reflection_partner")
        invariant = bool(channel.get("invariant_under_reflection"))
        if partner:
            if partner not in paths:
                errors.append(f"channel {name} names missing reflection partner {partner}")
                continue
            reflected = [reflect_edge(e, reflection) for e in paths[name]]
            partner_path = paths[partner]
            if len(reflected) != len(partner_path):
                errors.append(f"channel {name} reflected path length differs from {partner}")
            else:
                for idx, (a, b) in enumerate(zip(reflected, partner_path)):
                    if not same_edge(a, b):
                        errors.append(f"channel {name} reflected edge {idx} does not match {partner}: {a} vs {b}")
        elif invariant:
            reflected = [reflect_edge(e, reflection) for e in paths[name]]
            if len(reflected) != len(paths[name]) or any(not same_edge(a, b) for a, b in zip(reflected, paths[name])):
                errors.append(f"channel {name} is declared invariant but is not invariant under reflection")
        else:
            warnings.append(f"channel {name} has no reflection partner or invariant flag")

    for group in data.get("collapse_groups", []):
        if not group.get("must_share_limit", False):
            continue
        names = group.get("channels", [])
        limits: dict[str, list[tuple[tuple[float, ...], tuple[float, ...]]]] = {}
        for name in names:
            if name not in channels:
                errors.append(f"collapse group references missing channel {name}")
                continue
            raw_limit = channels[name].get("limit_edges")
            limits[name] = canonical_path(raw_limit) if raw_limit is not None else paths[name]
        if limits:
            first_name = next(iter(limits))
            first = limits[first_name]
            for name, limit in limits.items():
                if limit != first:
                    errors.append(f"collapse group limit mismatch: {name} has limit {limit}, expected {first_name} limit {first}")

    footprints: dict[str, list[tuple[float, ...]]] = {}
    for name, channel in channels.items():
        raw = channel.get("footprint_vertices")
        if raw is not None:
            footprints[name] = [vertex(v) for v in raw]
        else:
            footprints[name] = [v for v in path_vertices(paths[name]) if abs(v[int(reflection.get("axis", 2))] - float(reflection.get("offset", 0))) < 1e-12]
    if footprints:
        normalized = {name: sorted(set(vals)) for name, vals in footprints.items()}
        nonempty = [vals for vals in normalized.values() if vals]
        if nonempty and any(vals != nonempty[0] for vals in nonempty):
            errors.append(f"footprint mismatch across channels: {normalized}")

    valid = not errors
    return {
        "schema": "abducer.routea_edge_path_validation.v1",
        "candidate_id": data.get("candidate_id", "unknown"),
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "channels_checked": sorted(channels),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.candidate.read_text(encoding="utf-8"))
    report = validate(data)
    expected = data.get("expect_valid")
    if expected is not None:
        report["expected_valid"] = bool(expected)
        report["expectation_met"] = report["valid"] is bool(expected)
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)
    if expected is not None:
        return 0 if report["expectation_met"] else 1
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
