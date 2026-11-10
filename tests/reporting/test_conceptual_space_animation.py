# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for conceptual-space animation scene synthesis."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from generate_conceptual_space_animation import _build_animation_report, _render_html


def _scene_row(stage: str, *, label: str, source: str, target: str, route: str) -> dict:
    return {
        "stage": stage,
        "state": {
            "concept_count": 12,
            "object_count": 6,
            "hypothesis_state_counts": {"supported": 2},
            "lifecycle_totals": {"open": 1},
            "highlights": {
                "headline": f"{stage} sharpens the route",
                "leading_targets": [{"id": "tc.1", "label": "representation-target", "nature": "target-concept"}],
                "leading_invariants": [{"id": "inv.1", "label": "regularity", "nature": "invariant"}],
                "leading_bridge_objects": [{"id": "bo.1", "label": label, "object_type": "bridge_program"}],
                "supporting_dossiers": [
                    {
                        "id": "support.1",
                        "label": "positivity witness",
                        "object_type": "proof_sketch",
                        "content": {"route_synopsis": "Support positivity transfer into the measure object."},
                    }
                ],
                "primary_dossier": {
                    "id": "primary.1",
                    "label": label,
                    "object_type": "proof_sketch" if stage == "proof-sketch" else "bridge_program",
                    "score": 0.88,
                    "content": {
                        "route_synopsis": route,
                        "source_excerpt": source,
                        "target_excerpt": target,
                        "statement_delta": {
                            "model_shift": "functional -> measure",
                            "threshold_shift": "existence -> uniqueness",
                            "consequence_shift": "upgrade positivity into representation",
                            "typed_object_expectation": "representing measure",
                            "missing_witness_or_transport": "Show regularity and uniqueness of the measure witness.",
                            "route_synopsis": route,
                        },
                        "carrier_kind": "regular Borel measure",
                        "typing_status": "typed",
                        "bridge_definition": "Treat the representing measure as the carrier that transports positivity into representation.",
                        "conditional_claim": "If the measure object is regular, the representation target follows.",
                        "assumptions": [
                            "The source functional is positive.",
                            "The measure candidate is regular.",
                        ],
                        "obligations": [
                            "Construct the measure from positivity data.",
                            "Show uniqueness of the representing measure.",
                        ],
                        "lemmas": [
                            "Positivity yields a measure candidate.",
                            "Regularity upgrades the candidate into the target object.",
                        ],
                        "proof_outline": [
                            "Build the candidate measure.",
                            "Prove regularity and uniqueness.",
                        ],
                        "failure_diagnosis": "The route fails if regularity does not survive the construction.",
                        "counterfactual": "Allow the candidate measure to lose regularity. bridge-degrades-or-fails",
                    },
                },
            },
        },
    }


def test_conceptual_space_animation_builds_scenes_and_html() -> None:
    conceptual_report = {
        "metadata": {
            "kb": "KB/alpha-kb.kb.md",
            "kb_ref": "alpha-kb",
            "artifacts_dir": "artifacts/alpha-kb",
            "selected_run_id": "run-1",
        },
        "summary": {
            "current": {
                "concept_count": 18,
                "object_count": 9,
                "concept_nature_counts": {"bridge-object": 3},
                "object_type_counts": {"proof_sketch": 2, "bridge_program": 2},
                "lifecycle_totals": {"open": 1},
                "reasoning_type_counts": {"bridge-construction": 1, "proof-formalization": 1},
                "frontier": [{"id": "hyp.1", "label": "open measure uniqueness hypothesis", "status": "unresolved", "score": 0.66}],
                "highlights": {
                    "leading_targets": [{"id": "target.1", "label": "representation-target", "nature": "target-concept", "score": 0.91}],
                    "leading_invariants": [{"id": "inv.1", "label": "regularity", "nature": "invariant", "score": 0.84}],
                    "leading_bridge_objects": [{"id": "bridge.1", "label": "representing measure", "object_type": "bridge_program", "score": 0.88}],
                    "leading_proof_sketches": [{"id": "sk.1", "label": "recover representing measure", "object_type": "proof_sketch", "score": 0.82}],
                },
            }
        },
        "timeline": [
            _scene_row(
                "bridge-plan",
                label="representing measure",
                source="A positive functional should induce a measure candidate.",
                target="A unique regular Borel measure represents the functional.",
                route="Move from a positive functional to a regular Borel measure that represents it.",
            ),
            _scene_row(
                "proof-sketch",
                label="representing measure via constructive route",
                source="A positive functional should induce a measure candidate.",
                target="A unique regular Borel measure represents the functional.",
                route="Promote positivity into a typed measure object and discharge uniqueness.",
            ),
            _scene_row(
                "expert-paper",
                label="representation bridge: positivity => representing measure",
                source="A positive functional should induce a measure candidate.",
                target="A unique regular Borel measure represents the functional.",
                route="Render the route as an expert-facing mathematical note.",
            ),
        ],
    }

    report = _build_animation_report(conceptual_report, source_path="artifacts/alpha-kb/conceptual-dynamics.json")
    assert report["summary"]["scene_count"] >= 5
    assert report["summary"]["declared_node_count"] >= 8
    proof_scene = next(scene for scene in report["scenes"] if scene["stage"] == "proof-sketch")
    assert proof_scene["candidate_object"]["carrier_kind"] == "regular Borel measure"
    assert proof_scene["candidate_object"]["conditional_claim"] == "If the measure object is regular, the representation target follows."
    assert proof_scene["statement_delta"]["model_shift"] == "functional -> measure"
    assert proof_scene["obligations"][0] == "Construct the measure from positivity data."
    assert "regularity" in proof_scene["failure_diagnosis"]
    assert any(node["kind"] == "theorem-source" for node in proof_scene["nodes"])
    assert any(node["detail_body"] == "A positive functional should induce a measure candidate." for node in proof_scene["nodes"])
    assert any(edge["label"] == "target payoff" for edge in proof_scene["edges"])

    html = _render_html(report)
    assert "Conceptual Space Animation" in html
    assert "Reasoning Declaration" in html
    assert "Mathematical Delta" in html
    assert "Route Synopsis" in html
    assert "Assumptions" in html
    assert "Selected Node" in html
    assert "A positive functional should induce a measure candidate." in html
    assert "Allow the candidate measure to lose regularity." in html
    assert "resolveNodeLayout" in html
