# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for the epistemic process map generator."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "control-plane" / "meta" / "scripts"
COMMON_DIR = ROOT / "skills" / "common"
for path in (SCRIPT_DIR, COMMON_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_epistemic_process_map import build_process_model
from generate_epistemic_process_map import render_html
from generate_epistemic_process_map import render_markdown


def test_epistemic_process_map_covers_core_loops_and_surfaces() -> None:
    model = build_process_model()
    node_ids = {row["id"] for row in model["nodes"]}
    edge_ids = {row["id"] for row in model["edges"]}

    assert model["metadata"]["library"] == "Cytoscape.js"
    assert len(model["lanes"]) == 5
    assert len(model["process_spine"]) >= 6
    assert "kb" in node_ids
    assert "proof_queue" in node_ids
    assert "high_reward_watch" in node_ids
    assert "work_loop" in node_ids
    assert "meta" in node_ids
    assert "reasoning_surfaces" in node_ids
    assert all("glyph" in lane for lane in model["lanes"])
    assert any(node["id"] == "prove_cycle" and node["spine"] for node in model["nodes"])
    assert "e34" in edge_ids
    assert "e40" in edge_ids

    markdown = render_markdown(model)
    assert "# Epistemic Systems Visual Language" in markdown
    assert "## Epistemic Process Spine" in markdown
    assert "High-Reward Watch" in markdown
    assert "Cytoscape.js" in markdown

    html = render_html(model)
    assert "Cytoscape.js" in html
    assert "MathJax" in html
    assert "Epistemic Process" in html
    assert "System Channels" in html
    assert "Visibility Filters" in html
    assert "How To Read The Map" in html
    assert "High-Reward Watch" in html
