# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for macro-strategy report generation."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "reporting" / "kb-macro-proof-paper-writer" / "scripts"
COMMON_DIR = ROOT / "skills" / "common"
for path in (SCRIPT_DIR, COMMON_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_macro_strategy_report import build_strategy_report
from generate_macro_strategy_report import render_markdown


def test_macro_strategy_report_exposes_completion_gaps(tmp_path: Path) -> None:
    kb_path = tmp_path / "demo.kb.md"
    kb_path.write_text("```yaml\nid: st.thm.nonuniform-separation-target\ninformal: If NP is not contained in P/poly, then P != NP.\n```\n", encoding="utf-8")
    artifacts_dir = tmp_path / "artifacts" / "demo-kb"
    artifacts_dir.mkdir(parents=True)

    (artifacts_dir / "macro-proof-state.json").write_text(
        """{
  "main_conjecture": {
    "core_claim": "P != NP",
    "route_target_claim": "NP not in P/poly",
    "grounding_implication": "If NP is not contained in P/poly, then P != NP."
  },
  "leading_route": {
    "bridge_id": "bridge.001",
    "route_synopsis": "Move from the source theorem to a nonuniform separation target.",
    "invariant": "MCSP complexity profile",
    "target_claim_focus": "NP not in P/poly"
  },
  "supporting_routes": [
    {
      "bridge_id": "bridge.002",
      "route_synopsis": "Fallback route synopsis.",
      "missing_route_lemma": "Fallback missing lemma."
    }
  ],
  "status_assessment": {
    "evidence_count": 0
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "proof-sketches.json").write_text(
        """{
  "proof_sketches": [
    {
      "sketch_id": "psk.001",
      "bridge_id": "bridge.001",
      "sketch_score": 0.91,
      "conjectured_object": "MCSP witness family",
      "carrier_kind": "family of instances equipped with a witness measure",
      "proof_strategy_family": "invariant-lift-through-intermediate-object",
      "statement_delta": {
        "missing_witness_or_transport": "Route lemma for witness family."
      },
      "proof_obligations": [
        { "kind": "antecedent-realization", "requirement": "Source-to-object theorem." },
        { "kind": "invariant-preservation", "requirement": "Invariant transport theorem." },
        { "kind": "consequence-forcing", "requirement": "Payoff theorem." },
        { "kind": "operationalizability", "requirement": "Route lemma for witness family." }
      ]
    },
    {
      "sketch_id": "psk.005",
      "bridge_id": "bridge.001",
      "sketch_score": 0.87,
      "conjectured_object": "Gap-MCSP promise problem",
      "carrier_kind": "promise problem with explicit gap",
      "proof_strategy_family": "surrogate-reduction-transfer",
      "proof_obligations": [
        { "kind": "operationalizability", "requirement": "Make the threshold control explicit." }
      ]
    }
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "proof-queue.json").write_text(
        """{
  "metadata": { "kb_ref": "demo-kb", "pending_count": 1 },
  "entries": [
    { "queue_id": "proofq.demo-kb.001", "priority": 0.81, "title": "Leading route proof target" }
  ]
}""",
        encoding="utf-8",
    )

    report = build_strategy_report(kb_path=kb_path, artifacts_dir=artifacts_dir)
    assert report["summary_answer"]["headline"]
    assert report["metadata"]["bridge_id"] == "bridge.001"
    assert len(report["operationalizations"]) == 2
    titles = [row["title"] for row in report["missing_for_completion"]]
    assert any("Choose or prove equivalence" in title for title in titles)
    assert any("Route-specific magnification lemma" in row["title"] for row in report["completion_checklist"])

    md = render_markdown(report)
    assert "# Macro-Strategy Report for demo-kb" in md
    assert "## Abstract" in md
    assert "## Strategic Bottleneck" in md
    assert "## What Is Missing For Completion" in md
    assert "## Relevant References" in md
    assert "Source-to-object theorem." in md
    assert "Invariant transport theorem." in md
    assert "Payoff theorem." in md
