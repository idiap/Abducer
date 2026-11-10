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
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))
from generate_public_reasoning_trace_latex import render_tex  # noqa: E402


def test_every_inference_has_one_complete_stable_dossier() -> None:
    packet = json.loads((ROOT / "tests/fixtures/reasoning_trace/generated/theorem_proof_delivery.packet.json").read_text())
    tex = render_tex(packet)
    assert tex.count(r"\begin{TraceDossier}") == len(packet["inferences"])
    normalized = tex.replace(r"\allowbreak{}", "")
    for event in packet["inferences"]:
        escaped_id = event["event_id"].replace("_", r"\_")
        assert normalized.count(f": {escaped_id}") == 1
    for field in ("Typed premises", "Transformation / operator", "Bounded public warrant", "Conclusion", "Uncertainty", "Scope before / after / model / regime", "Artifact integrity status", "Scientific epistemic status", "Workflow disposition", "Authority"):
        assert tex.count(field) >= len(packet["inferences"])


def test_control_events_are_separate_from_scientific_dossiers() -> None:
    packet = json.loads((ROOT / "tests/fixtures/reasoning_trace/generated/theorem_proof_delivery.packet.json").read_text())
    control_ids = [row["event_id"] for row in packet["timeline"] if row["event_family"] in {"control", "authorization", "gate"}]
    inference_ids = {row["event_id"] for row in packet["inferences"]}
    assert inference_ids.isdisjoint(control_ids)
    tex = render_tex(packet)
    assert "Control-only events appear in the lifecycle appendix and are not scientific claims" in tex
    assert "Complete chronological lifecycle ledger" in tex


def test_negative_paths_and_crosslinks_receive_equal_visibility() -> None:
    packet = json.loads((ROOT / "tests/fixtures/reasoning_trace/generated/theorem_proof_delivery.packet.json").read_text())
    tex = render_tex(packet)
    assert tex.count(r"\hypertarget{trace-alternative-") == len(packet["alternatives_and_failures"])
    assert r"\hyperlink{trace-evidence-" in tex
    assert "TRACE INCOMPLETE" not in tex
