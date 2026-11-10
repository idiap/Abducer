# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for meta reflection report generation."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "control-plane" / "meta" / "scripts"
COMMON_DIR = ROOT / "skills" / "common"
MACRO_SCRIPT_DIR = ROOT / "skills" / "reporting" / "kb-macro-proof-paper-writer" / "scripts"
for path in (SCRIPT_DIR, COMMON_DIR, MACRO_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_meta_reflection_report import build_meta_reflection_report
from generate_meta_reflection_report import render_markdown
from generate_meta_reflection_report import render_tex


def test_meta_reflection_report_tracks_shifts_and_persistence(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo-kb"
    artifacts_dir.mkdir(parents=True)

    (artifacts_dir / "epistemic-hardness.json").write_text(
        """{
  "epistemic_difficulty_summary": "The original problem is hard because it spans incompatible proof regimes and sparse explicit dependencies."
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "macro-proof-state.json").write_text(
        """{
  "main_conjecture": {
    "core_claim": "P != NP",
    "route_target_claim": "NP not in P/poly"
  },
  "leading_route": {
    "candidate_object": "MCSP witness family",
    "route_consistency_note": "The witness-family and Gap-MCSP operationalizations are not yet aligned."
  },
  "references": [
    {
      "statement_id": "st.thm.nonuniform-separation-target",
      "title": "Nonuniform separation target",
      "excerpt": "If NP is not contained in P/poly, then P != NP."
    }
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "macro-strategy-report.json").write_text(
        """{
  "narrative": {
    "bottleneck": "The bottleneck is the leading magnification bridge.",
    "subresult_value": "A source-to-object theorem or transport theorem would already be valuable."
  },
  "references": [
    {
      "statement_id": "st.src",
      "title": "Leading-route source",
      "role": "Leading-route source",
      "detail": "Barely nontrivial lower bounds may magnify into strong consequences."
    }
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "proof-cycle-summary.json").write_text(
        """{
  "metadata": {
    "pending_count": 3,
    "proved_count": 0
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "end-to-end-proof-plausibility.json").write_text(
        """{
  "signals": {
    "evidence_count": 0
  },
  "decision": {
    "plausible_solution_detected": false
  },
  "critics": [
    {
      "critic_id": "adversarial-pressure",
      "title": "Adversarial-Pressure Critic",
      "score": 1,
      "rationale": "No adversarial evidence has yet accumulated."
    },
    {
      "critic_id": "novelty-discipline",
      "title": "Novelty-Discipline Critic",
      "score": 1,
      "rationale": "No terminal result has been audited against prior art."
    }
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "promising-directions-report.json").write_text(
        """{
  "most_promising_directions": [
    {
      "novelty_points": [
        "The top route isolates a typed bridge object.",
        "The route is theorem-pair specific."
      ]
    }
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "search-space-tree.json").write_text(
        """{
  "frontier": {
    "resume": [
      {
        "bridge_id": "bridge.001",
        "policy": "resume-with-deeper-proof",
        "priority": 0.75,
        "route_synopsis": "Move from the source theorem to a nonuniform target."
      }
    ]
  }
}""",
        encoding="utf-8",
    )

    report = build_meta_reflection_report(
        artifacts_dir=artifacts_dir,
        perspective="epistemic",
        interpretation="balanced",
    )

    assert report["metadata"]["kb_ref"] == "demo-kb"
    assert report["metadata"]["perspective"] == "epistemic"
    assert report["current_proof_state_interpretation"]["headline"]
    assert len(report["shifts_of_understanding"]) >= 4
    assert any(row["label"] == "persistence" for row in report["shifts_of_understanding"])
    assert any("Adversarial-Pressure" in row["title"] for row in report["persistent_difficulties"])

    md = render_markdown(report)
    assert "# Meta Reflection Report for demo-kb" in md
    assert "## Original Hardness" in md
    assert "## Shifts Of Understanding" in md
    assert "## Meta Judgment" in md
    assert "The bottleneck is the leading magnification bridge." in md

    tex = render_tex(report)
    assert "\\section{Original Hardness}" in tex
    assert "\\section{Shifts Of Understanding}" in tex
    assert "\\section{Meta Judgment}" in tex


def test_meta_reflection_report_surfaces_high_reward_continuation(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo-kb"
    artifacts_dir.mkdir(parents=True)

    (artifacts_dir / "macro-proof-state.json").write_text(
        """{
  "main_conjecture": {
    "core_claim": "P != NP",
    "route_target_claim": "NP not in P/poly"
  },
  "leading_route": {
    "candidate_object": "MCSP witness family"
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "macro-strategy-report.json").write_text(
        """{
  "narrative": {
    "bottleneck": "The bottleneck is still the leading bridge."
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "proof-cycle-summary.json").write_text(
        """{
  "metadata": {
    "pending_count": 2,
    "proved_count": 1
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "end-to-end-proof-plausibility.json").write_text(
        """{
  "signals": {
    "evidence_count": 1
  },
  "decision": {
    "plausible_solution_detected": false
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "promising-directions-report.json").write_text(
        """{"most_promising_directions": []}""",
        encoding="utf-8",
    )
    (artifacts_dir / "search-space-tree.json").write_text(
        """{"frontier": {"resume": []}}""",
        encoding="utf-8",
    )
    (artifacts_dir / "high-reward-watch.json").write_text(
        """{
  "metadata": {
    "kb_ref": "demo-kb",
    "watch_version": 1
  },
  "signals": [
    {
      "signal_id": "highreward.demo-kb.001",
      "status": "active",
      "result_id": "mathlib.demo-kb.003",
      "title": "Witness family transport theorem",
      "major_subresult_score": 12,
      "recommended_extension_cycles": 4,
      "continuation_rationale": "The theorem seeded a live local follow-up programme.",
      "follow_up_prove_queue_ids": ["proofq.demo-kb.030"],
      "follow_up_discovery_branch_ids": ["disclayer.demo-kb.high-reward.witness"]
    }
  ]
}""",
        encoding="utf-8",
    )

    report = build_meta_reflection_report(artifacts_dir=artifacts_dir)
    assert report["high_reward_continuation"]["signal_id"] == "highreward.demo-kb.001"

    md = render_markdown(report)
    assert "## High-Reward Continuation" in md
    assert "Witness family transport theorem" in md

    tex = render_tex(report)
    assert "\\section{High-Reward Continuation}" in tex
