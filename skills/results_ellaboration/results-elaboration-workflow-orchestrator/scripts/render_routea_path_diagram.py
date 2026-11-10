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
"""Render a simple SVG diagram for Route A edge-list path candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


COLORS = ["#d95f02", "#1b9e77", "#7570b3", "#e7298a", "#66a61e"]


def project(v: list[float], scale: float = 80.0) -> tuple[float, float]:
    # Draw x1 horizontally and x2 vertically; time shifts lightly upward.
    return 80 + scale * v[1], 220 - scale * v[2] - 18 * (v[0] - 1)


def line(edge: Any, color: str, label: str) -> str:
    a, b = edge
    x1, y1 = project(a)
    x2, y2 = project(b)
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="3" marker-end="url(#arrow)"><title>{label}</title></line>'
    )


def render(data: dict[str, Any]) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="620" height="320" viewBox="0 0 620 320">',
        "<defs><marker id=\"arrow\" markerWidth=\"8\" markerHeight=\"8\" refX=\"6\" refY=\"3\" orient=\"auto\"><path d=\"M0,0 L0,6 L6,3 z\" fill=\"#333\"/></marker></defs>",
        '<rect width="100%" height="100%" fill="#fbfbfb"/>',
        f'<text x="20" y="28" font-family="serif" font-size="18">Route A path candidate: {data.get("candidate_id", "unknown")}</text>',
        '<line x1="70" y1="220" x2="560" y2="220" stroke="#aaa" stroke-dasharray="4 4"/>',
        '<text x="565" y="224" font-size="12" fill="#666">x2=0</text>',
    ]
    for idx, channel in enumerate(data.get("channels", [])):
        color = COLORS[idx % len(COLORS)]
        name = channel.get("name", f"ch{idx}")
        parts.append(f'<text x="20" y="{58 + 18 * idx}" font-size="13" fill="{color}">{name}</text>')
        for edge in channel.get("edges", []):
            parts.append(line(edge, color, name))
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.candidate.read_text(encoding="utf-8"))
    svg = render(data)
    out = args.output or args.candidate.with_suffix(".svg")
    out.write_text(svg, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
