# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for human-readable interpretation report generation.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"

if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from generate_interpretation_reports import _discovery_report
from generate_interpretation_reports import _collect_math_surface
from generate_interpretation_reports import _process_report


def test_generate_interpretation_reports_from_partial_artifacts(tmp_path: Path) -> None:
    """
    Concept: Validates that generate interpretation reports from partial artifacts.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    artifacts = tmp_path / "artifacts" / "mini"
    artifacts.mkdir(parents=True, exist_ok=True)

    (artifacts / "connection-analysis.json").write_text(
        json.dumps(
            {
                "stats": {"statement_count": 2},
                "top_interventions": [
                    {
                        "statement_id": "st.thm.a",
                        "score": 0.77,
                        "rationale": "central connector",
                    }
                ],
                "connection_candidates": [
                    {"from_id": "st.def.a", "to_id": "st.thm.a", "score": 0.62}
                ],
            }
        ),
        encoding="utf-8",
    )

    (artifacts / "coherence-report.json").write_text(
        json.dumps(
            {
                "coherence_profile": {"global_coherence": 0.41},
                "hypothesis_coherence": [
                    {
                        "hypothesis_id": "phyp.test.001",
                        "kind": "bridge-link",
                        "coherence_delta_global": 0.08,
                        "explanatory_power_local": 0.55,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    analysis = json.loads((artifacts / "connection-analysis.json").read_text(encoding="utf-8"))
    coherence = json.loads((artifacts / "coherence-report.json").read_text(encoding="utf-8"))

    process_text = _process_report(
        kb="KB/test.kb.md",
        artifacts_dir=artifacts,
        analysis=analysis,
        coherence=coherence,
        entrypoints={},
        pathways={},
        hardness={},
        bridges={},
        strategies={},
        proof_sketches={
            "proof_sketches": [
                {
                    "sketch_id": "psk.001",
                    "conjecture_id": "conj.001",
                    "strategy_id": "strat.001",
                    "proof_strategy_family": "invariant-lift-through-intermediate-object",
                    "sketch_score": 0.73,
                    "target_consequence_schema": "NP-not-in-P/poly",
                    "preserved_invariant": "MCSP complexity profile",
                    "barrier_scope": "none",
                    "proof_obligations": [
                        {"requirement": "Show that the conjectured object preserves `MCSP complexity profile` from the source side."}
                    ],
                    "counterfactual_test": {"intervention": "Remove invariant preservation"},
                }
            ]
        },
        hypothesis_eval={},
        hypothesis_loop={},
        revision={},
        conjectures={
            "abstraction_conjectures": [
                {
                    "conjecture_id": "conj.001",
                    "abstraction_type": "intermediate-complexity-measure",
                    "abstraction_label": "MCSP complexity potential",
                    "priority": 0.77,
                    "gap_target": "missing-intermediate-abstraction",
                    "target_consequence_schema": "NP-not-in-P/poly",
                    "preserved_invariant": "MCSP complexity profile",
                    "definitional_profile": {
                        "necessary_attributes": [
                            {"attribute": "preserves `MCSP complexity profile`"},
                        ]
                    },
                    "counterfactual_probes": [
                        {"intervention": "Remove invariant preservation"}
                    ],
                }
            ]
        },
    )
    discovery_text = _discovery_report(
        kb="KB/test.kb.md",
        artifacts_dir=artifacts,
        analysis=analysis,
        coherence=coherence,
        entrypoints={},
        pathways={},
        hardness={},
        bridges={},
        strategies={},
        proof_sketches={
            "proof_sketches": [
                {
                    "sketch_id": "psk.001",
                    "conjecture_id": "conj.001",
                    "strategy_id": "strat.001",
                    "proof_strategy_family": "invariant-lift-through-intermediate-object",
                    "target_consequence_schema": "NP-not-in-P/poly",
                    "support_antecedent_schema": "MCSP-nonuniform-circuits-lower-bound",
                    "preserved_invariant": "MCSP complexity profile",
                    "proof_obligations": [
                        {"requirement": "Show that the conjectured object preserves `MCSP complexity profile` from the source side."}
                    ],
                    "abort_conditions": [
                        "Abort if the conjectured object cannot be defined without collapsing back into a generic topic label."
                    ],
                }
            ]
        },
        hypothesis_eval={},
        hypothesis_loop={},
        revision={},
        conjectures={
            "abstraction_conjectures": [
                {
                    "conjecture_id": "conj.001",
                    "abstraction_type": "intermediate-complexity-measure",
                    "abstraction_label": "MCSP complexity potential",
                    "mathematical_object_role": "Tracks the missing lift.",
                    "priority": 0.77,
                    "gap_target": "missing-intermediate-abstraction",
                    "definitional_profile": {
                        "necessary_attributes": [
                            {"attribute": "preserves `MCSP complexity profile`"},
                        ],
                        "sufficient_attribute_sets": [
                            {"label": "minimal core set", "attributes": ["preserves `MCSP complexity profile`", "forces `NP-not-in-P/poly`"]},
                        ],
                    },
                    "counterfactual_probes": [
                        {"intervention": "Remove invariant preservation", "expected_bridge_effect": "bridge-degrades-or-fails"}
                    ],
                }
            ]
        },
    )

    assert "# Reasoning Process Report" in process_text
    assert "Stage Snapshot" in process_text
    assert "# Discovery Interpretation Report" in discovery_text
    assert "Current Discovery Posture" in discovery_text
    assert "st.thm.a" in discovery_text
    assert "Conjecture Snapshot" in process_text
    assert "Proof Sketch Snapshot" in process_text
    assert "Conjectured Mathematical Abstractions" in discovery_text
    assert "necessary=preserves `MCSP complexity profile`" in process_text
    assert "counterfactual=Remove invariant preservation" in process_text
    assert "sketch counterfactual=Remove invariant preservation" in process_text
    assert "necessary attributes: preserves `MCSP complexity profile`" in discovery_text
    assert "Proof Sketch Interpretation" in discovery_text
    assert "first proof obligation: Show that the conjectured object preserves `MCSP complexity profile` from the source side." in discovery_text


def test_collect_math_surface_prefers_theorem_level_signatures() -> None:
    """
    Concept: Validates that collect math surface prefers theorem level signatures.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    analysis = {
        "top_interventions": [
            {
                "statement_id": "st.thm.karp-lipton",
                "concept_focus": ["circuit-complexity", "PH-collapse"],
                "concept_profile": {
                    "implication_signatures": ["NP-in-P/poly-implies-PH-collapse"],
                    "consequence_signatures": ["PH-collapse-to-Sigma2"],
                    "claim_signatures": ["PH-collapse"],
                },
            }
        ],
        "connection_candidates": [
            {
                "concept_evidence": ["circuit-complexity", "lower-bound"],
                "from_profile": {"implication_signatures": ["PIT-in-P-implies-lower-bounds"]},
                "to_profile": {"consequence_signatures": ["NEXP-vs-P/poly-or-Permanent-lower-bound"]},
            }
        ],
    }

    math_surface = _collect_math_surface(analysis)

    assert "NP-in-P/poly-implies-PH-collapse" in math_surface
    assert "PH-collapse-to-Sigma2" in math_surface
    assert "circuit-complexity" not in math_surface
