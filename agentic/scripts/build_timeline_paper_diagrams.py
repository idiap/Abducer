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
"""Build paper diagrams from the timeline-paper blueprint."""

from __future__ import annotations

from agentic_common import ROOT, load_json_object, rel, stable_id, utc_now, write_json
from build_timeline_paper_blueprint import OUT_JSON as BLUEPRINT_JSON


OUT_DIR = ROOT / "agentic/reports/timeline_paper_diagrams"
OUT_JSON = OUT_DIR / "latest.json"
OUT_TEX = OUT_DIR / "latest.tex"
SCHEMA = ROOT / "agentic/spec/timeline_paper_diagram.schema.json"


def tex_label(value: str) -> str:
    text = str(value or "")
    for src, dst in {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }.items():
        text = text.replace(src, dst)
    return text


def build_argument_nodes(blueprint: dict) -> list[dict]:
    return [
        {"node_id": "target", "label": "Target commitments", "role": "problem_commitment", "source": "target literature report"},
        {"node_id": "route", "label": "Route pressure", "role": "strategy_pressure", "source": "macro strategy and timeline story"},
        {"node_id": "object", "label": blueprint.get("primary_mathematical_object", "Active object"), "role": "mathematical_object", "source": "paper blueprint"},
        {"node_id": "finite_test", "label": "Finite criterion", "role": "local_test", "source": "formal derivation"},
        {"node_id": "worked_example", "label": "Worked calculation", "role": "calculation", "source": "endpoint or finite-algebra artifacts"},
        {"node_id": "claim", "label": "Smallest honest claim", "role": "contribution", "source": "contribution matrix"},
        {"node_id": "handoff", "label": "Validation handoff", "role": "transfer_obligation", "source": "strategy judge"},
    ]


def build_edges() -> list[dict]:
    return [
        {"source": "target", "target": "route", "meaning": "The target problem creates route pressure.", "edge_type": "motivates"},
        {"source": "route", "target": "object", "meaning": "The timeline narrows route pressure into a mathematical object.", "edge_type": "selects"},
        {"source": "object", "target": "finite_test", "meaning": "The object supports a local finite positivity/obstruction criterion.", "edge_type": "defines"},
        {"source": "finite_test", "target": "worked_example", "meaning": "The criterion demands a concrete computation or falsifier.", "edge_type": "requires"},
        {"source": "worked_example", "target": "claim", "meaning": "The computation determines the honest paper claim.", "edge_type": "supports"},
        {"source": "claim", "target": "handoff", "meaning": "The claim remains bounded by transfer obligations.", "edge_type": "bounded_by"},
        {"source": "handoff", "target": "route", "meaning": "Failed transfer forces backtracking or demotion.", "edge_type": "demotion_feedback"},
    ]


def render_tikz(nodes: list[dict], edges: list[dict]) -> str:
    labels = {node["node_id"]: tex_label(node["label"]) for node in nodes}
    return rf"""
\begin{{figure}}[t]
\centering
\begin{{tikzpicture}}[
  node distance=1.0cm and 0.8cm,
  box/.style={{draw, rounded corners, align=center, text width=2.8cm, minimum height=0.8cm}},
  arrow/.style={{-{{Latex[length=2mm]}}, thick}},
  warn/.style={{-{{Latex[length=2mm]}}, thick, dashed}}
]
\node[box] (target) {{{labels['target']}}};
\node[box, right=of target] (route) {{{labels['route']}}};
\node[box, right=of route] (object) {{{labels['object']}}};
\node[box, below=of object] (finite_test) {{{labels['finite_test']}}};
\node[box, right=of finite_test] (worked_example) {{{labels['worked_example']}}};
\node[box, right=of worked_example] (claim) {{{labels['claim']}}};
\node[box, above=of claim] (handoff) {{{labels['handoff']}}};
\draw[arrow] (target) -- (route);
\draw[arrow] (route) -- (object);
\draw[arrow] (object) -- (finite_test);
\draw[arrow] (finite_test) -- (worked_example);
\draw[arrow] (worked_example) -- (claim);
\draw[arrow] (claim) -- (handoff);
\draw[warn] (handoff) to[bend left=16] (route);
\end{{tikzpicture}}
\caption{{Organizing diagram generated from the paper blueprint. It separates target commitments, the active mathematical object, the local criterion, the worked calculation, the smallest honest claim, and the validation handoff. Dashed feedback marks demotion or backtracking if the transfer obligation fails.}}
\label{{fig:timeline-paper-blueprint}}
\end{{figure}}
"""


def build_report() -> dict:
    blueprint = load_json_object(BLUEPRINT_JSON)
    nodes = build_argument_nodes(blueprint)
    edges = build_edges()
    tikz = render_tikz(nodes, edges)
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "schema": rel(SCHEMA),
        "status": "timeline_paper_diagrams_ready",
        "diagram_id": stable_id("timeline-paper-diagram", blueprint.get("blueprint_id"), len(nodes), len(edges)),
        "source_blueprint": rel(BLUEPRINT_JSON),
        "diagrams": [
            {
                "diagram_id": "argument_flow",
                "diagram_type": "argument_flow",
                "nodes": nodes,
                "edges": edges,
                "tikz": tikz,
                "caption": "Generated argument-flow diagram for the paper blueprint.",
            }
        ],
        "artifacts": {"json": rel(OUT_JSON), "tex": rel(OUT_TEX)},
        "epistemic_status": "diagram_validation_needed",
        "validation_handoff": "python agentic/scripts/validate_timeline_paper_diagrams.py",
    }


def main() -> int:
    report = build_report()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_JSON, report)
    OUT_TEX.write_text(report["diagrams"][0]["tikz"], encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_TEX)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
