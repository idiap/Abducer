# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for reasoning-dynamics extraction and visualization metrics.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from generate_reasoning_dynamics import _build_dynamics


def test_reasoning_dynamics_extracts_graph_process_and_concept_metrics(tmp_path: Path) -> None:
    """
    Concept: Validates that reasoning dynamics extracts graph process and concept metrics.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    repo = tmp_path
    artifacts = repo / "artifacts" / "mini"
    phyp_dir = repo / "phyp"
    artifacts.mkdir(parents=True, exist_ok=True)
    phyp_dir.mkdir(parents=True, exist_ok=True)

    analysis_path = artifacts / "connection-analysis.json"
    analysis_path.write_text(
        json.dumps(
            {
                "stats": {
                    "statement_count": 3,
                    "edge_count": 2,
                    "missing_dependency_count": 1,
                },
                "concept_graph": {
                    "nodes": [{"id": "c1"}, {"id": "c2"}, {"id": "c3"}],
                    "relations": [
                        {"relation": "defines"},
                        {"relation": "uses"},
                        {"relation": "defines"},
                    ],
                },
                "connection_candidates": [{"id": "x1"}],
                "top_interventions": [{"statement_id": "st.1"}],
            }
        ),
        encoding="utf-8",
    )

    phyp_path = phyp_dir / "mini.proof-hypotheses.yaml"
    phyp_path.write_text(
        yaml.safe_dump(
            {
                "hypotheses": [
                    {"id": "phyp.1", "kind": "bridge-link", "status": "pending"},
                    {"id": "phyp.2", "kind": "intermediate-invariant", "status": "pending"},
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    coherence_path = artifacts / "coherence-report.json"
    coherence_path.write_text(
        json.dumps(
            {
                "coherence_profile": {
                    "global_coherence": 0.52,
                    "consistency": 0.71,
                    "integration": 0.63,
                    "tension": 0.18,
                    "explanatory_unification": 0.49,
                },
                "typed_coherence_graph": {
                    "nodes": [{"id": "n1"}, {"id": "n2"}],
                    "edges": [{"id": "e1"}],
                    "relation_counts": {"supports": 1, "explains": 1},
                },
            }
        ),
        encoding="utf-8",
    )

    nodes = {
        "run:r1": {"id": "run:r1", "node_type": "run", "label": "run:r1", "meta": {}},
        "agent:kb-orchestrator": {
            "id": "agent:kb-orchestrator",
            "node_type": "agent",
            "label": "kb-orchestrator",
            "meta": {},
        },
        "step:r1:1": {"id": "step:r1:1", "node_type": "step", "label": "Running stage: connect", "meta": {}},
        "stage:r1:connect": {"id": "stage:r1:connect", "node_type": "stage", "label": "connect", "meta": {}},
        "artifact:analysis": {
            "id": "artifact:analysis",
            "node_type": "artifact",
            "label": "connection-analysis.json",
            "meta": {"path": str(analysis_path)},
        },
        "artifact:phyp": {
            "id": "artifact:phyp",
            "node_type": "artifact",
            "label": "mini.proof-hypotheses.yaml",
            "meta": {"path": str(phyp_path)},
        },
        "artifact:coherence": {
            "id": "artifact:coherence",
            "node_type": "artifact",
            "label": "coherence-report.json",
            "meta": {"path": str(coherence_path)},
        },
    }
    edges = {
        "e-exec": {
            "id": "e-exec",
            "source": "run:r1",
            "target": "agent:kb-orchestrator",
            "edge_type": "executed_by",
            "label": "kb-orchestrator",
            "meta": {},
        },
        "e-stage-start": {
            "id": "e-stage-start",
            "source": "step:r1:1",
            "target": "stage:r1:connect",
            "edge_type": "stage_started",
            "label": "connect",
            "meta": {},
        },
        "e-invoke": {
            "id": "e-invoke",
            "source": "stage:r1:connect",
            "target": "agent:kb-orchestrator",
            "edge_type": "invokes_agent",
            "label": "kb-proof-connector",
            "meta": {},
        },
        "e-out-analysis": {
            "id": "e-out-analysis",
            "source": "stage:r1:connect",
            "target": "artifact:analysis",
            "edge_type": "emits_output",
            "label": "connection_analysis_json",
            "meta": {},
        },
        "e-out-phyp": {
            "id": "e-out-phyp",
            "source": "stage:r1:connect",
            "target": "artifact:phyp",
            "edge_type": "emits_output",
            "label": "proof_hypotheses_yaml",
            "meta": {},
        },
        "e-stage-end": {
            "id": "e-stage-end",
            "source": "step:r1:1",
            "target": "stage:r1:connect",
            "edge_type": "stage_completed",
            "label": "connect",
            "meta": {},
        },
        "e-declare": {
            "id": "e-declare",
            "source": "run:r1",
            "target": "artifact:coherence",
            "edge_type": "declares_output",
            "label": "coherence_report_json",
            "meta": {},
        },
    }

    node_ids: list[str] = []
    edge_ids: list[str] = []
    states: list[dict[str, object]] = []

    def add_state(
        *,
        index: int,
        event_type: str,
        added_node_ids: list[str],
        added_edge_ids: list[str],
        description: str,
    ) -> None:
        """
        Concept: Appends one synthetic state to the reasoning-dynamics timeline under test.
        Contribution: Builds a controlled evolution sequence so graph-dynamics metrics can be validated deterministically.
        """
        node_ids.extend(added_node_ids)
        edge_ids.extend(added_edge_ids)
        states.append(
            {
                "index": index,
                "timestamp": f"2026-03-11T12:00:0{index}Z",
                "run_key": "r1",
                "event_type": event_type,
                "description": description,
                "added_node_ids": added_node_ids,
                "added_edge_ids": added_edge_ids,
                "node_ids": sorted(node_ids),
                "edge_ids": sorted(edge_ids),
            }
        )

    add_state(
        index=0,
        event_type="log_started",
        added_node_ids=["run:r1", "agent:kb-orchestrator"],
        added_edge_ids=["e-exec"],
        description="kb-orchestrator started log run.md",
    )
    add_state(
        index=1,
        event_type="stage_started",
        added_node_ids=["step:r1:1", "stage:r1:connect"],
        added_edge_ids=["e-stage-start", "e-invoke"],
        description="Running stage: connect",
    )
    add_state(
        index=2,
        event_type="step",
        added_node_ids=["artifact:analysis", "artifact:phyp"],
        added_edge_ids=["e-out-analysis", "e-out-phyp"],
        description="Output artifacts emitted",
    )
    add_state(
        index=3,
        event_type="stage_completed",
        added_node_ids=[],
        added_edge_ids=["e-stage-end"],
        description="Completed stage: connect",
    )
    add_state(
        index=4,
        event_type="declared_output",
        added_node_ids=["artifact:coherence"],
        added_edge_ids=["e-declare"],
        description="Declared output: coherence_report_json",
    )

    evolution = {
        "states": states,
        "final_graph": {
            "nodes": list(nodes.values()),
            "edges": list(edges.values()),
        },
    }

    report = _build_dynamics(evolution=evolution, artifact_root=repo)
    summary = report["summary"]
    operation_totals = summary["operation_totals"]
    final_concept = summary["concept_evolution"]["final_state"]

    assert summary["state_count"] == 5
    assert operation_totals["stage_started"] == 1
    assert operation_totals["stage_completed"] == 1
    assert operation_totals["declared_output"] == 1
    assert operation_totals["emits_output"] == 2
    assert operation_totals["invokes_agent"] == 1
    assert final_concept["concept_graph_nodes"] == 3
    assert final_concept["concept_graph_relations"] == 3
    assert final_concept["coherence_global"] == 0.52
    assert final_concept["hypothesis_total"] == 2
    assert final_concept["concept_topology_index"] > 0.0
