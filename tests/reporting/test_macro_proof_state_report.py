# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for macro-proof state report generation."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "reporting" / "kb-macro-proof-paper-writer" / "scripts"
COMMON_DIR = ROOT / "skills" / "common"
for path in (SCRIPT_DIR, COMMON_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_macro_proof_state_report import build_report
from generate_macro_proof_state_report import render_tex


def test_macro_proof_state_report_keeps_main_conjecture_grounding(tmp_path: Path) -> None:
    kb_path = tmp_path / "demo.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "```yaml",
                "id: st.def.item",
                "title: Definition of P",
                "informal: P is the class of languages decidable in deterministic polynomial time.",
                "```",
                "",
                "```yaml",
                "id: st.def.item-2",
                "title: Definition of NP",
                "informal: NP is the class of languages whose yes instances have polynomial-size certificates verifiable in polynomial time.",
                "```",
                "",
                "```yaml",
                "id: st.def.np-completeness",
                "title: Definition of NP-completeness",
                "informal: A language is NP-complete if it lies in NP and every problem in NP reduces to it.",
                "```",
                "",
                "```yaml",
                "id: st.def.item-5",
                "title: Definition of P/poly",
                "informal: P/poly is the class of languages decided by polynomial-size circuit families.",
                "```",
                "",
                "```yaml",
                "id: st.thm.cook-levin-sat-is-np-complete-cook1971",
                "title: Cook-Levin",
                "informal: SAT is NP-complete.",
                "```",
                "",
                "```yaml",
                "id: st.thm.nonuniform-separation-target",
                "title: Nonuniform separation target",
                "informal: If NP not subseteq P/poly, then P != NP.",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )

    artifacts_dir = tmp_path / "artifacts" / "demo-kb"
    artifacts_dir.mkdir(parents=True)
    (artifacts_dir / "expert-hypothesis-paper.json").write_text(
        """{
  "bridge_portfolio": [
    {
      "bridge_id": "bridge.001",
      "priority": 0.82,
      "route_synopsis": "Move from the magnification program to a nonuniform separation consequence.",
      "source_statement_id": "st.src",
      "target_statement_id": "st.tgt",
      "preserved_invariant": "MCSP witness profile",
      "proof_strategy_family": "invariant-lift-through-intermediate-object",
      "family_rationale": "Lift through an intermediate witness object.",
      "abstraction_label": "MCSP witness family",
      "carrier_kind": "family of instances equipped with a witness measure",
      "conditional_proposition": "If the bridge is realized, then NP not in P/poly follows.",
      "mathematical_assumptions": ["The witness family exists."],
      "proof_obligations": ["Show the witness family forces the target separation."],
      "candidate_lemmas": ["Route lemma: the witness family transports the lower bound."],
      "missing_route_lemma": "Route lemma: the witness family transports the lower bound.",
      "negative_route": "Drop the source witness data and the bridge fails.",
      "failure_diagnosis": "The bridge collapses into topical overlap without the route lemma.",
      "statement_delta": {
        "source_claim_focus": "barely nontrivial lower bound",
        "target_claim_focus": "NP not in P/poly",
        "source_theorem_excerpt": "A barely nontrivial lower bound may magnify.",
        "target_theorem_excerpt": "The target theorem yields NP not in P/poly.",
        "model_shift": "nonuniform-circuits",
        "threshold_shift": "major separation consequence",
        "consequence_shift": "upgrade a weak lower bound into NP not in P/poly"
      }
    }
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "proof-sketches.json").write_text(
        """{
  "proof_sketches": [
    {
      "bridge_id": "bridge.001",
      "proof_outline_steps": [
        { "objective": "Define the witness family." },
        { "objective": "Use it to derive NP not in P/poly." }
      ],
      "candidate_lemmas": [
        { "statement": "Source-to-object lemma." }
      ],
      "proof_obligations": [
        { "requirement": "Show the object preserves the invariant." }
      ]
    }
  ]
}""",
        encoding="utf-8",
    )
    (artifacts_dir / "hypothesis-evaluation.json").write_text(
        """{
  "metadata": { "evidence_count": 0 },
  "summary": { "verdict_counts": { "supported": 2, "inconclusive": 3 } }
}""",
        encoding="utf-8",
    )
    # Supply real local KB anchors so the current interpretability gate admits
    # the item; the assertions below exercise report grounding, not deferral.
    (artifacts_dir / "proof-queue.json").write_text(
        """{
  "metadata": { "kb_ref": "demo-kb", "queue_version": 2, "pending_count": 1 },
  "entries": [
    {
      "queue_id": "proofq.demo-kb.001",
      "status": "pending",
      "priority": 0.77,
      "title": "Witness family route",
      "candidate_object": "MCSP witness family",
      "source_statement_id": "st.thm.cook-levin-sat-is-np-complete-cook1971",
      "source_excerpt": "SAT is NP-complete.",
      "target_statement_id": "st.thm.nonuniform-separation-target",
      "target_excerpt": "If NP not subseteq P/poly, then P != NP.",
      "conjecture_statement": "There exists an admissible witness family yielding NP not in P/poly.",
      "missing_route_lemma": "Route lemma: the witness family transports the lower bound."
    }
  ]
}""",
        encoding="utf-8",
    )

    report = build_report(kb_path=kb_path, artifacts_dir=artifacts_dir)
    assert report["main_conjecture"]["core_claim"] == "P != NP"
    assert report["main_conjecture"]["route_target_claim"] == "NP not in P/poly"
    assert "P/poly" in report["main_conjecture"]["grounding_implication"]
    assert "P != NP" in report["main_conjecture"]["grounding_implication"]
    assert report["leading_route"]["bridge_id"] == "bridge.001"
    assert report["proof_frontier"][0]["queue_id"] == "proofq.demo-kb.001"

    tex = render_tex(report)
    assert "Macro-Proof State Report for" in tex
    assert "\\section{Introduction}" in tex
    assert "\\section{Reduction Strategy}" in tex
    assert "\\section{Main Conjecture}" in tex
    assert "\\section{Conditional Macro-Proof}" in tex
    assert "\\section{Leading Route}" in tex
    assert "\\section{Relevant Local References}" in tex
    assert "NP not in P/poly" in tex
