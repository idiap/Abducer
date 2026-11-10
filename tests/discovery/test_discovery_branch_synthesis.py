# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for discovery-branch synthesis and follow-up agenda generation."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
DISCOVERY_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-discovery-cycle" / "scripts"

for path in (COMMON_DIR, DISCOVERY_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_discovery_branch_synthesis import build_report, render_markdown
from proof_queue import default_queue, proof_queue_paths, save_proof_queue


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def test_synthesis_normalizes_target_ids_and_builds_agenda(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    executions_dir = artifacts_dir / "discovery-branch-executions"
    executions_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    semantic_report_path = executions_dir / "semantic.json"
    invariant_report_path = executions_dir / "invariant.json"
    _write_json(
        semantic_report_path,
        {
            "metadata": {"branch_id": "disclayer.demo.family.semantic-bridge", "status": "completed-state-delta"},
            "branch": {
                "target_id": "semantic bridge",
                "target_label": "Semantic Bridge Prompt",
                "routing_priority": 2.3,
                "required_move": "Bridge a local definition to a biconditional theorem.",
            },
            "local_frontier": {
                "linked_queue_count": 3,
                "mathlib_hits": [{"title": "Cook and Reckhow 1979"}],
            },
            "execution": {
                "candidate_claims": [
                    "Local definitional object D has property P if and only if global characterization condition Q holds."
                ],
                "theorem_candidates": [
                    {
                        "title": "Semantic bridge theorem",
                        "statement": "Local definitional object D has property P if and only if global characterization condition Q holds.",
                        "concretization_status": "concrete",
                        "concretization_score": 5,
                    }
                ],
                "state_delta": {
                    "delta_kind": "theorem-candidate",
                    "promotable_theorem_count": 1,
                    "max_concretization_score": 5,
                },
            },
        },
    )
    _write_json(
        invariant_report_path,
        {
            "metadata": {"branch_id": "disclayer.demo.pattern.invariant-discovery", "status": "completed-state-delta"},
            "branch": {
                "target_id": "invariant-discovery",
                "target_label": "Invariant Discovery Prompt",
                "routing_priority": 6.8,
                "required_move": "Identify the preserved quantity organizing the blocked frontier.",
            },
            "local_frontier": {
                "linked_queue_count": 7,
                "mathlib_hits": [{"title": "Oliveira and Santhanam 2018"}],
            },
            "execution": {
                "candidate_claims": [
                    "There exists a monotone witness measure that survives every legitimate route variant."
                ],
                "concept_revisions": [
                    {
                        "label": "invariant-discovery",
                        "revision": "Identify the preserved quantity organizing the blocked frontier.",
                        "epistemic_gain": "Refines the discovery programme before prove resumes.",
                    }
                ],
                "state_delta": {
                    "delta_kind": "concept-revision",
                    "promotable_theorem_count": 0,
                    "max_concretization_score": 0,
                },
            },
        },
    )

    _write_json(
        artifacts_dir / "discovery-branch-queue.json",
        {
            "metadata": {"kb_ref": "demo"},
            "branches": [
                {
                    "branch_id": "disclayer.demo.family.semantic-bridge",
                    "status": "completed",
                    "linked_breakthrough_families": ["semantic bridge"],
                    "linked_obstruction_classes": ["characterization-bridge"],
                },
                {
                    "branch_id": "disclayer.demo.pattern.invariant-discovery",
                    "status": "completed",
                    "linked_breakthrough_families": ["abstraction-search"],
                    "linked_obstruction_classes": ["carrier-realization"],
                },
            ],
        },
    )
    _write_json(
        executions_dir / "index.json",
        {
            "metadata": {"kb_ref": "demo", "execution_count": 2},
            "executions": [
                {
                    "branch_id": "disclayer.demo.family.semantic-bridge",
                    "artifact_json": str(semantic_report_path),
                    "artifact_md": str(executions_dir / "semantic.md"),
                },
                {
                    "branch_id": "disclayer.demo.pattern.invariant-discovery",
                    "artifact_json": str(invariant_report_path),
                    "artifact_md": str(executions_dir / "invariant.md"),
                },
            ],
        },
    )

    report = build_report(artifacts_dir=artifacts_dir, kb_ref="demo", repo_root=repo_root)

    assert report["metadata"]["ready_for_prove_count"] == 1
    assert report["metadata"]["ready_for_discovery_count"] == 1
    by_branch = {row["branch_id"]: row for row in report["next_programmes"]}
    assert by_branch["disclayer.demo.family.semantic-bridge"]["mode"] == "prove-candidate"
    assert by_branch["disclayer.demo.family.semantic-bridge"]["agenda_bucket"] == "ready_for_prove"
    assert by_branch["disclayer.demo.family.semantic-bridge"]["promotable_theorem_count"] == 1
    assert by_branch["disclayer.demo.pattern.invariant-discovery"]["mode"] == "discovery-candidate"
    assert by_branch["disclayer.demo.pattern.invariant-discovery"]["agenda_bucket"] == "ready_for_discovery"
    assert by_branch["disclayer.demo.pattern.invariant-discovery"]["state_delta_kind"] == "concept-revision"
    assert by_branch["disclayer.demo.pattern.invariant-discovery"]["promotable_theorem_count"] == 0

    rendered = render_markdown(report)
    assert "## Ready For Prove" in rendered
    assert "## Ready For Discovery" in rendered
    assert "Promotable theorem candidates: 1" in rendered
    assert "Local definitional object D has property P if and only if global characterization condition Q holds." in rendered
