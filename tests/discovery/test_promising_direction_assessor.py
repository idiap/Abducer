# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for promising-directions assessment synthesis."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-promising-direction-assessor" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_promising_directions_report import build_report, render_markdown, render_tex


def _bridge(bridge_id: str, target_id: str, priority: float) -> dict:
    return {
        "bridge_id": bridge_id,
        "bridge_type": "magnification bridge",
        "source_statement_id": "st.src",
        "target_statement_id": target_id,
        "priority": priority,
        "signals": {
            "sketch_score": 0.91,
            "mathematical_specificity": 0.88,
            "evidence_signal": 0.19,
            "sketch_operationalization": 1.0,
            "proof_readiness": 1.0,
        },
        "abstraction_label": "typed witness family",
        "carrier_kind": "family of instances equipped with a monotone witness measure",
        "preserved_invariant": "witness complexity profile",
        "route_synopsis": f"Move from st.src toward {target_id} with a typed witness family.",
        "proof_strategy_family": "invariant-lift-through-intermediate-object",
        "family_rationale": "Lift the source regime through a typed invariant.",
        "source_excerpt": "A barely nontrivial lower bound implies a major consequence.",
        "target_excerpt": f"Target theorem body for {target_id}.",
        "statement_delta": {
            "source_claim_focus": "barely nontrivial lower bound",
            "target_claim_focus": f"major consequence at {target_id}",
            "missing_witness_or_transport": f"Show the witness family reaches {target_id}.",
        },
        "missing_route_lemma": f"Show the witness family reaches {target_id}.",
        "failure_diagnosis": "The route fails if the witness family is only topical overlap.",
        "negative_route": "Allow the carrier to ignore the source-side content and only preserve topical overlap.",
        "abort_conditions": [
            "Abort if the carrier cannot be defined on the theorem pair.",
            "Abort if the route-specific lemma fails.",
        ],
        "proof_obligations": [
            "Build the typed witness family from the source theorem.",
            f"Show the witness family forces {target_id}.",
        ],
        "expert_actions": [
            "Discharge the route-specific lemma.",
            "Run the counterfactual probe.",
        ],
        "linked_hypothesis_ids": ["hyp.1", "hyp.2"],
    }


def test_promising_direction_report_selects_top_and_next_best_routes() -> None:
    expert = {
        "metadata": {"kb_ref": "alpha-kb", "selected_run_id": "run-1"},
        "bridge_portfolio": [
            _bridge("bridge.001", "st.tgt.1", 0.81),
            _bridge("bridge.002", "st.tgt.2", 0.77),
            {
                **_bridge("bridge.003", "st.other", 0.61),
                "abstraction_label": "different carrier",
                "source_statement_id": "st.other.src",
            },
        ],
    }
    hypothesis_eval = {
        "metadata": {"evidence_count": 0},
        "summary": {"verdict_counts": {"supported": 2, "inconclusive": 1}},
        "results": [
            {
                "hypothesis_id": "hyp.1",
                "verdict": "supported",
                "confidence": 0.82,
                "recommended_action": "promote-or-retest-with-deduction",
            },
            {
                "hypothesis_id": "hyp.2",
                "verdict": "supported",
                "confidence": 0.73,
                "recommended_action": "promote-or-retest-with-deduction",
            },
            {
                "hypothesis_id": "hyp.3",
                "verdict": "inconclusive",
                "priority": 0.68,
                "target_statement_id": "st.tgt.2",
                "recommended_action": "run-another-abduce-deduce-round",
                "reasons": ["strong cross-component potential"],
            },
        ],
    }

    report = build_report(expert, hypothesis_eval, artifacts_dir=ROOT / "artifacts" / "alpha-kb", top_k=2)
    assert report["summary"]["top_direction_id"] == "bridge.001"
    assert report["summary"]["next_best_direction_id"] == "bridge.002"
    assert report["next_best_direction"]["target_statement_id"] == "st.tgt.2"
    assert "programmatic" in report["novelty_assessment"]["verdict"]

    markdown = render_markdown(report)
    assert "Most Promising Directions" in markdown
    assert "Next Best Direction To Explore" in markdown
    assert "Recommended Probe" in markdown
    assert "mathematical specificity" in markdown
    assert "sketch operationalization" in markdown

    tex = render_tex(report)
    assert "Promising Directions Assessment for" in tex
    assert "\\section{Most Promising Directions}" in tex
    assert "\\section{Next Best Direction To Explore}" in tex
