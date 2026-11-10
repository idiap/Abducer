# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for discovery-process slide generation."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "control-plane" / "meta" / "scripts"
COMMON_DIR = ROOT / "skills" / "common"
for path in (SCRIPT_DIR, COMMON_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_discovery_process_slides import build_discovery_process_slides
from generate_discovery_process_slides import render_markdown


def test_discovery_process_slides_include_concepts_connections_and_queue(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo-kb"
    artifacts_dir.mkdir(parents=True)

    (artifacts_dir / "work-state.json").write_text(
        """{
  "metadata": {
    "cycle_count": 2,
    "next_phase": "prove"
  },
  "latest": {
    "phase": "discovery",
    "detail": "Queued 3 proof targets."
  },
  "plausibility": {
    "plausibility_score": 0.41
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "meta-reflection-report.json").write_text(
        """{
  "metadata": {
    "perspective": "epistemic"
  },
  "original_hardness": {
    "summary": "The problem spans incompatible proof regimes.",
    "hardness_elements": [
      {"detail": "Cross-regime proof movement remains difficult."}
    ]
  },
  "current_proof_state_interpretation": {
    "headline": "The current proof state is a conditional programme.",
    "detail": "The bottleneck is the leading bridge."
  },
  "persistent_difficulties": [
    {"detail": "Representation alignment remains open."},
    {"detail": "Evidence is still thin."}
  ],
  "meta_judgment": {
    "headline": "Understanding improved but the proof is still open.",
    "detail": "The route is sharper but still unresolved.",
    "next_question": "Can the bridge object be fixed?"
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "macro-proof-state.json").write_text(
        """{
  "main_conjecture": {
    "core_claim": "P != NP",
    "route_target_claim": "NP not in P/poly",
    "grounding_implication": "If NP is not in P/poly, then P != NP."
  },
  "leading_route": {
    "candidate_object": "MCSP witness family",
    "invariant": "MCSP complexity profile",
    "target_claim_focus": "major consequences such as NP not in P/poly",
    "missing_route_lemma": "Route lemma for witness family."
  },
  "status_assessment": {
    "assessment": "The route is coherent but open.",
    "evidence_count": 0
  }
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "proof-queue.json").write_text(
        """{
  "metadata": { "pending_count": 3 },
  "entries": [
    {
      "title": "MCSP witness family: major consequences such as NP not in P/poly",
      "priority": 0.9,
      "claim_text": "A typed witness family yields NP not in P/poly.",
      "missing_route_lemma": "Route lemma for witness family."
    }
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "promising-directions-report.json").write_text(
        """{
  "most_promising_directions": [
    {"route_synopsis": "Route one.", "novelty_points": ["Typed witness family.", "Theorem-pair route."]},
    {"route_synopsis": "Route two."},
    {"route_synopsis": "Route three."}
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "conceptual-dynamics.json").write_text(
        """{
  "timeline": [
    {
      "stage": "connect.analyze",
      "state": {
        "highlights": {
          "headline": "targets mild-lower-bounds-imply-major-separation",
          "introduced_targets": [
            {"label": "mild-lower-bounds-imply-major-separation"},
            {"label": "MCSP-near-threshold-nonuniform-circuit-lower-bound"}
          ]
        }
      }
    },
    {
      "stage": "bridge-plan",
      "state": {
        "highlights": {
          "headline": "bridge-plan headline"
        }
      }
    },
    {
      "stage": "conjecture",
      "state": {
        "highlights": {
          "headline": "Gap-MCSP promise problem appears",
          "introduced_bridge_objects": [
            {"label": "Gap-MCSP promise problem"},
            {"label": "MCSP witness family"}
          ]
        }
      }
    },
    {
      "stage": "proof-sketch",
      "state": {
        "highlights": {
          "stage_proof_sketches": [
            {"label": "MCSP witness family via strat.001"}
          ]
        }
      }
    },
    {
      "stage": "expert-paper",
      "state": {
        "highlights": {
          "supported_hypotheses": [
            {"label": "phyp.demo.001"}
          ]
        }
      }
    }
  ]
}""",
        encoding="utf-8",
    )

    deck = build_discovery_process_slides(artifacts_dir=artifacts_dir)
    assert deck["metadata"]["kb_ref"] == "demo-kb"
    assert deck["metadata"]["slide_count"] >= 8

    md = render_markdown(deck)
    assert "# Discovery Process Slides for demo-kb" in md
    assert "# Slide 3 - What Changed In Framing" in md
    assert "MCSP witness family" in md
    assert "Gap-MCSP promise problem" in md
    assert "Route one." in md
    assert "A typed witness family yields NP not in P/poly." in md
