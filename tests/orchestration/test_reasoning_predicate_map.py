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

import json
import subprocess
import sys
from pathlib import Path

from agentic.scripts import build_reasoning_predicate_map as compiler

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "agentic/registries/reasoning_flow_catalog.yaml"
STATE = ROOT / "agentic/state/reasoning_predicate_map.json"
SOURCE = ROOT / "agentic/reasoning_flows/all-reasoning.pmap"


# REUSE-IgnoreStart
def test_doc_render_retains_legal_notice_and_detects_stale_body(tmp_path, monkeypatch):
    target = tmp_path / "predicate-map.md"
    monkeypatch.setattr(compiler, "DOC_OUTPUT", target)
    source = "map abducer {\n}\n"
    body = compiler.render_doc({}, source)
    preamble = "<!--\nSPDX-License-Identifier: MIT\n-->\n\n"
    target.write_text(preamble + "stale body\n", encoding="utf-8")
    rendered = compiler.render_doc({}, source)
    assert rendered == preamble + body
    assert rendered != target.read_text(encoding="utf-8")


# REUSE-IgnoreEnd


def test_predicate_map_is_fresh_and_covers_the_reasoning_system() -> None:
    result = subprocess.run(
        [sys.executable, "agentic/scripts/build_reasoning_predicate_map.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    assert {row["reasoning"] for row in payload["entries"]} == {
        row["id"] for row in catalog["flows"]
    }
    assert all(row["output"] and row["output_id"] for row in payload["entries"])


def test_predicate_map_collapses_steps_and_preserves_handoffs() -> None:
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    entries = {row["reasoning"]: row for row in payload["entries"]}
    conceptual = entries["conceptual_hypothesis_exploration_loop"]
    assert conceptual["predicates"] == [
        "constrain",
        "transfer",
        "assume",
        "test",
        "calibrate",
    ]
    assert conceptual["output"] == "refinement_status"
    assert conceptual["connects_to"] == ["abducer_work_loop", "release_promotion_loop"]
    source = SOURCE.read_text(encoding="utf-8")
    assert source.startswith("map abducer {\n")
    assert "predicate-map" not in source
    assert (
        "reasoning::conceptual_hypothesis_exploration_loop "
        "-constrain, transfer, assume, test, calibrate> "
        "output::conceptual_hypothesis_exploration_loop.refinement_status"
    ) in source
