# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for stage-aware discovery graph explorer assembly.

Concept: Captures the intended behavior of the conceptual discovery-space visualizer under deterministic fixtures.
Contribution: Keeps the bridge, conjecture, and hardness layers visible in the explorer as the framework evolves.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from generate_discovery_graph_explorer import _build_graph_data, _render_html


def test_discovery_graph_explorer_builds_stage_aware_conceptual_graph() -> None:
    """
    Concept: Validates that the discovery explorer fuses landscape, hypothesis, bridge, conjecture, and hardness layers into one staged graph.
    Contribution: Guards the main conceptual promise of the explorer: showing discovery objects as they enter the reasoning space.
    """

    analysis = {
        "concept_graph": {
            "nodes": [
                {"id": "statement:st.a", "type": "statement", "label": "st.a"},
                {"id": "concept:alpha", "type": "concept", "label": "alpha"},
            ],
            "relations": [
                {"from": "statement:st.a", "to": "concept:alpha", "relation": "uses", "weight": 0.8},
            ],
        }
    }
    phyp = {
        "hypotheses": [
            {
                "id": "phyp.001",
                "kind": "bridge-link",
                "status": "needs-testing",
                "priority": 0.73,
                "support_statement_id": "st.a",
                "target_statement_id": "st.b",
                "preserved_invariant": "transfer witness",
            }
        ]
    }
    coherence = {
        "typed_coherence_graph": {
            "nodes": [{"id": "statement:st.b", "type": "statement", "label": "st.b"}],
            "edges": [{"from": "statement:st.a", "to": "statement:st.b", "relation": "supports", "weight": 0.6}],
        }
    }
    bridges = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.001",
                "from_id": "st.a",
                "to_id": "st.b",
                "bridge_type": "structural support bridge",
                "bridge_score": 0.61,
            }
        ]
    }
    conjectures = {
        "abstraction_conjectures": [
            {
                "conjecture_id": "conj.001",
                "bridge_id": "bridge.001",
                "from_id": "st.a",
                "to_id": "st.b",
                "abstraction_type": "intermediate-complexity-measure",
                "abstraction_label": "transfer witness family",
                "priority": 0.69,
                "anchor_concepts": ["alpha frontier"],
                "statement_delta": {
                    "route_synopsis": "Move from st.a to st.b through a transfer witness family.",
                    "model_shift": "functional -> representation",
                    "consequence_shift": "upgrade `positive-functional` into `representation-target`",
                },
                "mathematical_specification": {
                    "definition_template": "A transfer witness family packages the source-side positivity data into a representation object.",
                    "conditional_claim": "If the witness family exists and preserves the invariant, the target representation follows.",
                    "proof_obligation_templates": ["show the witness family realizes the target representation"],
                },
            }
        ]
    }
    proof_sketches = {
        "proof_sketches": [
            {
                "sketch_id": "psk.001",
                "title": "Transfer witness route",
                "bridge_id": "bridge.001",
                "conjecture_id": "conj.001",
                "source_statement_id": "st.a",
                "target_statement_id": "st.b",
                "proof_strategy_family": "invariant-lift-through-intermediate-object",
                "sketch_score": 0.81,
                "carrier_kind": "transfer witness family",
                "typing_status": "typed",
                "preserved_invariant": "transfer witness",
                "statement_delta": {
                    "route_synopsis": "Lift the source statement into a transport witness and then force the target statement.",
                    "model_shift": "source regime -> target regime",
                    "missing_witness_or_transport": "Prove that the transfer witness actually carries the source theorem into the target theorem.",
                    "source_theorem_excerpt": "Statement st.a supplies the source-side content.",
                    "target_theorem_excerpt": "Statement st.b is the target-side payoff.",
                },
                "proof_obligations": [
                    {"requirement": "Construct the transfer witness from st.a."},
                    {"requirement": "Show the witness implies st.b."},
                ],
                "candidate_lemmas": [
                    {"statement": "Source-to-object lemma: st.a induces the transfer witness."},
                    {"statement": "Payoff lemma: the witness forces st.b."},
                ],
                "proof_outline_steps": [
                    {"objective": "Build the witness."},
                    {"objective": "Transport the invariant."},
                ],
                "mathematical_argument": {
                    "bridge_definition": "Treat the transfer witness as the typed proof object mediating st.a and st.b.",
                    "proposition": "If the transfer witness exists and preserves the invariant, then st.b follows.",
                    "lemma_chain": [
                        "Source-to-object lemma: st.a induces the transfer witness.",
                        "Transport lemma: the invariant is preserved along the route.",
                    ],
                    "failure_mode": "The route fails if the witness does not preserve the transfer invariant.",
                },
                "counterfactual_test": {
                    "intervention": "Delete the invariant-preserving clause from the witness.",
                    "expected_bridge_effect": "bridge-degrades-or-fails",
                },
            }
        ]
    }
    hardness = {
        "essential_elements": [
            {
                "name": "Barrier Stack Constraints",
                "severity": "high",
                "evidence_ids": ["st.b"],
            }
        ]
    }
    expert_paper = {
        "recommended_bridges": [
            {
                "bridge_id": "bridge.001",
                "abstraction_label": "transfer witness family",
                "source_excerpt": "Statement st.a supplies the source theorem content.",
                "target_excerpt": "Statement st.b is the target theorem payoff.",
                "route_synopsis": "Move from st.a to st.b through the transfer witness family.",
                "carrier_kind": "transfer witness family",
                "typing_status": "typed",
                "conditional_proposition": "If the witness family is realized, then st.b follows.",
                "proof_obligations": ["Prove the witness family exists."],
                "candidate_lemmas": ["Route lemma: the witness carries st.a into st.b."],
                "failure_diagnosis": "The route collapses if the witness family is only topical.",
                "negative_route": "Allow the witness to ignore the source-side content.",
                "expert_actions": ["Prove the witness family exists."],
                "statement_delta": {
                    "source_claim_focus": "st.a",
                    "target_claim_focus": "st.b",
                    "model_shift": "source regime -> target regime",
                },
            }
        ]
    }
    reasoning_dynamics = {
        "summary": {
            "concept_evolution": {
                "updates": [
                    {
                        "artifact_kind": "connection-analysis",
                        "timestamp": "2026-03-12T12:00:00Z",
                        "metrics": {"concept_graph_nodes": 2},
                    },
                    {
                        "artifact_kind": "phyp",
                        "timestamp": "2026-03-12T12:00:01Z",
                        "metrics": {"hypothesis_total": 1},
                    },
                    {
                        "artifact_kind": "coherence-report",
                        "timestamp": "2026-03-12T12:00:02Z",
                        "metrics": {"coherence_global": 0.33},
                    },
                    {
                        "artifact_kind": "epistemic-hardness",
                        "timestamp": "2026-03-12T12:00:03Z",
                        "metrics": {"hardness_elements": 1},
                    },
                    {
                        "artifact_kind": "bridge-plan",
                        "timestamp": "2026-03-12T12:00:04Z",
                        "metrics": {"bridge_program_count": 1},
                    },
                    {
                        "artifact_kind": "concept-gap-abstractions",
                        "timestamp": "2026-03-12T12:00:05Z",
                        "metrics": {"abstraction_conjecture_count": 1},
                    },
                    {
                        "artifact_kind": "proof-sketches",
                        "timestamp": "2026-03-12T12:00:06Z",
                        "metrics": {"proof_sketch_count": 1},
                    },
                ]
            }
        }
    }
    statement_index = {
        "st.a": {
            "id": "st.a",
            "kind": "theorem",
            "informal": "Every source object admits a transfer witness.",
        },
        "st.b": {
            "id": "st.b",
            "kind": "theorem",
            "informal": "Every admissible transfer witness yields the target representation.",
        },
    }

    graph = _build_graph_data(
        analysis=analysis,
        phyp=phyp,
        coherence=coherence,
        bridges=bridges,
        conjectures=conjectures,
        proof_sketches=proof_sketches,
        hardness=hardness,
        expert_paper=expert_paper,
        reasoning_dynamics=reasoning_dynamics,
        statement_index=statement_index,
    )

    node_ids = {row["id"] for row in graph["nodes"]}
    assert "hypothesis:phyp.001" in node_ids
    assert "bridge:bridge.001" in node_ids
    assert "conjecture:conj.001" in node_ids
    assert "proof-sketch:psk.001" in node_ids
    assert "abstraction-family:intermediate-complexity-measure" in node_ids
    assert "hardness:barrier-stack-constraints" in node_ids

    families = {row["family"] for row in graph["nodes"]}
    assert {"concept", "proposition", "proof-object"} <= families

    edge_types = {row["type"] for row in graph["edges"]}
    assert {"motivates", "targets", "proposes", "instantiates", "obstructs", "grounds"} <= edge_types
    assert "hypothesis-source" not in edge_types
    assert "bridge-target" not in edge_types

    stage_order = [row["stage_key"] for row in graph["states"]]
    assert stage_order == ["analysis", "phyp", "coherence", "hardness", "bridge-plan", "conjecture", "proof-sketch"]

    final_state = graph["states"][-1]
    assert "coherence_global" in final_state["metrics"]
    assert final_state["metrics"]["bridge_program_count"] == 1
    assert final_state["metrics"]["proof_sketch_count"] == 1
    assert graph["metadata"]["timeline_state_count"] == 7

    proof_node = next(row for row in graph["nodes"] if row["id"] == "proof-sketch:psk.001")
    assert proof_node["detail"]["source_excerpt"] == "Statement st.a supplies the source-side content."
    assert proof_node["detail"]["target_excerpt"] == "Statement st.b is the target-side payoff."
    assert proof_node["detail"]["statement_delta"]["model_shift"] == "source regime -> target regime"
    assert proof_node["detail"]["obligations"][0] == "Construct the transfer witness from st.a."
    assert any("Source-to-object lemma" in row for row in proof_node["detail"]["lemmas"])
    assert proof_node["detail"]["counterfactual"] == "Delete the invariant-preserving clause from the witness. / bridge-degrades-or-fails"

    bridge_node = next(row for row in graph["nodes"] if row["id"] == "bridge:bridge.001")
    assert bridge_node["detail"]["source_excerpt"] == "Statement st.a supplies the source theorem content."
    assert bridge_node["detail"]["failure_diagnosis"] == "The route collapses if the witness family is only topical."
    assert bridge_node["detail"]["expert_actions"] == ["Prove the witness family exists."]

    statement_node = next(row for row in graph["nodes"] if row["id"] == "statement:st.a")
    assert statement_node["detail"]["statement_excerpt"] == "Every source object admits a transfer witness."
    assert "Move from st.a to st.b through the transfer witness family." in statement_node["detail"]["related_routes"]
    assert "Prove the witness family exists." in statement_node["detail"]["expert_actions"]

    concept_node = next(row for row in graph["nodes"] if row["id"] == "concept:alpha")
    assert concept_node["detail"]["statement_excerpt"] == "Every source object admits a transfer witness."
    assert concept_node["detail"]["related_routes"]
    assert any("st.a" in row for row in concept_node["detail"]["linked_objects"])

    html = _render_html("alpha", graph)
    assert "Selected Node" in html
    assert "Route synopsis" in html
    assert "Statement" in html
    assert "Related routes" in html
    assert "Linked objects" in html
    assert "Expert actions" in html
    assert "Mathematical delta" in html
    assert "Counterfactual probe" in html
