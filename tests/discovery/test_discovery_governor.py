# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for the scripted discovery governor and its integrations."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
DISCOVERY_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-discovery-cycle" / "scripts"
GOVERNOR_SCRIPT_DIR = ROOT / "skills" / "evaluation" / "kb-discovery-governor" / "scripts"

for path in (COMMON_DIR, DISCOVERY_SCRIPT_DIR, GOVERNOR_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from discovery_branch_queue import load_discovery_branch_state
from discovery_branch_queue import save_discovery_branch_state
from execute_discovery_branches import execute_active_discovery_branches
from generate_discovery_governor_report import apply_governor_to_branch_state
from generate_discovery_governor_report import build_report
from generate_discovery_governor_report import discovery_governor_paths
from generate_discovery_governor_report import write_report
from enqueue_discovery_programmes import build_promotions
from problem_mathlib import default_mathlib, mathlib_paths, save_mathlib_index
from proof_queue import default_queue, enqueue_entries, proof_queue_paths, save_proof_queue


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def test_discovery_governor_activates_high_value_branch_and_freezes_weak_branch(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-a",
                "title": "Blocked route A",
                "priority": 0.92,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Construct a witness family forcing the target.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "status": "blocked",
            },
            {
                "queue_key": "bridge.002|st.tgt.2|route-b",
                "title": "Blocked route B",
                "priority": 0.35,
                "bridge_id": "bridge.002",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Investigate the route.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.2",
                "status": "blocked",
            },
        ],
    )
    save_proof_queue(queue, json_path=artifacts_dir / "proof-queue.json", md_path=artifacts_dir / "proof-queue.md")

    _write_json(
        artifacts_dir / "discovery-breakthrough-profile.json",
        {
            "metadata": {"kb_ref": "demo"},
            "profiles": [
                {"obstruction_class": "carrier-realization", "major_subresult_type": "bridge object/tool"},
                {"obstruction_class": "target-grounding", "major_subresult_type": "research recommendation"},
            ],
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-queue.json",
        {
            "metadata": {"kb_ref": "demo"},
            "branches": [
                {
                    "branch_id": "disclayer.demo.family.realization",
                    "status": "active",
                    "target_label": "Carrier Realization Prompt",
                    "routing_priority": 2.4,
                    "linked_queue_ids": ["proofq.demo.001"],
                    "linked_breakthrough_families": ["realization"],
                    "linked_obstruction_classes": ["carrier-realization"],
                    "required_move": "Realize an explicit witness family.",
                    "abstraction_required": "A typed witness family with admissibility conditions.",
                    "minimal_theorem_shape": "If the source theorem holds, construct an admissible witness family preserving the invariant and forcing the target theorem.",
                    "required_questions": ["What admissibility conditions are necessary?"],
                    "expected_deliverables": ["One theorem candidate."],
                    "anti_patterns": ["Renaming the carrier without a construction."],
                    "negative_outputs": ["Prove that no admissible witness family of this form can exist."],
                    "sample_theorem_targets": ["Construct the admissible witness family."],
                    "attempt_count": 0,
                },
                {
                    "branch_id": "disclayer.demo.family.target-grounding",
                    "status": "active",
                    "target_label": "Target Grounding Prompt",
                    "routing_priority": 0.2,
                    "linked_queue_ids": ["proofq.demo.002"],
                    "linked_breakthrough_families": ["bridge-specificity"],
                    "linked_obstruction_classes": ["target-grounding"],
                    "required_move": "Restate the target theorem as a recommendation.",
                    "abstraction_required": "",
                    "minimal_theorem_shape": "",
                    "required_questions": [],
                    "expected_deliverables": [],
                    "anti_patterns": ["Rediscovering the target theorem."],
                    "negative_outputs": [],
                    "sample_theorem_targets": [],
                    "attempt_count": 2,
                    "last_outcome_summary": "Repeated analysis pass with no theorem candidate.",
                },
            ],
        },
    )

    state = load_discovery_branch_state(artifacts_dir / "discovery-branch-queue.json", kb_ref="demo")
    report = build_report(artifacts_dir=artifacts_dir, kb_ref="demo", activate_top_k=1)
    apply_governor_to_branch_state(state, report=report, activate_top_k=1)
    save_discovery_branch_state(
        state,
        json_path=artifacts_dir / "discovery-branch-queue.json",
        md_path=artifacts_dir / "discovery-branch-queue.md",
    )

    decisions = {row["branch_id"]: row for row in report["branch_decisions"]}
    assert decisions["disclayer.demo.family.realization"]["decision"] in {"deepen", "major_subresult_candidate"}
    assert decisions["disclayer.demo.family.target-grounding"]["decision"] == "freeze"

    refreshed = load_discovery_branch_state(artifacts_dir / "discovery-branch-queue.json", kb_ref="demo")
    rows = {row["branch_id"]: row for row in refreshed["branches"]}
    assert rows["disclayer.demo.family.realization"]["status"] == "active"
    assert rows["disclayer.demo.family.target-grounding"]["status"] == "deprioritized"


def test_discovery_branch_execution_respects_governor_deprioritization(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-a",
                "title": "Blocked route A",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "Route A",
                "conjecture_statement": "Construct a witness family.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source lower bound excerpt.",
                "target_excerpt": "Target separation excerpt.",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Witness realization lemma",
                "status": "blocked",
            },
            {
                "queue_key": "bridge.002|st.tgt.2|route-b",
                "title": "Blocked route B",
                "priority": 0.55,
                "bridge_id": "bridge.002",
                "claim_type": "route-conjecture",
                "claim_text": "Route B",
                "conjecture_statement": "Investigate route B.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.2",
                "source_excerpt": "Source lower bound excerpt.",
                "target_excerpt": "Secondary target excerpt.",
                "candidate_object": "Weak carrier",
                "preserved_invariant": "weak profile",
                "missing_route_lemma": "Weak route lemma",
                "status": "blocked",
            },
        ],
    )
    save_proof_queue(queue, json_path=artifacts_dir / "proof-queue.json", md_path=artifacts_dir / "proof-queue.md")

    mathlib = default_mathlib(kb_ref="demo")
    mathlib_json, mathlib_md = mathlib_paths(repo_root, "demo")
    save_mathlib_index(mathlib, json_path=mathlib_json, md_path=mathlib_md)

    _write_json(
        artifacts_dir / "discovery-branch-queue.json",
        {
            "metadata": {"kb_ref": "demo"},
            "branches": [
                {
                    "branch_id": "disclayer.demo.family.realization",
                    "status": "active",
                    "target_id": "realization",
                    "target_label": "Carrier Realization Prompt",
                    "routing_priority": 2.1,
                    "linked_queue_ids": ["proofq.demo.001"],
                    "linked_breakthrough_families": ["realization"],
                    "linked_obstruction_classes": ["carrier-realization"],
                    "required_move": "Realize the witness family.",
                    "abstraction_required": "An explicit witness family.",
                    "minimal_theorem_shape": "If the source theorem holds, construct a witness family forcing the target.",
                    "required_questions": ["How is the witness family constructed?"],
                    "expected_deliverables": ["Theorem candidate."],
                    "anti_patterns": ["Renaming the carrier."],
                    "negative_outputs": ["No such witness family exists under the local constraints."],
                    "sample_theorem_targets": ["Construct the witness family."],
                    "search_modes": ["explicit carrier construction"],
                },
                {
                    "branch_id": "disclayer.demo.family.target-grounding",
                    "status": "active",
                    "target_id": "target-grounding",
                    "target_label": "Target Grounding Prompt",
                    "routing_priority": 0.3,
                    "linked_queue_ids": ["proofq.demo.002"],
                    "linked_breakthrough_families": ["bridge-specificity"],
                    "linked_obstruction_classes": ["target-grounding"],
                    "required_move": "Restate the target.",
                    "abstraction_required": "",
                    "minimal_theorem_shape": "",
                    "required_questions": [],
                    "expected_deliverables": [],
                    "anti_patterns": ["Rediscovering the target theorem."],
                    "negative_outputs": [],
                    "sample_theorem_targets": [],
                    "search_modes": ["target restatement"],
                },
            ],
        },
    )
    governor_report = {
        "metadata": {"kb_ref": "demo"},
        "branch_decisions": [
            {
                "branch_id": "disclayer.demo.family.realization",
                "decision": "deepen",
                "value_score": 0.82,
                "value_band": "high-value",
                "governor_rank": 1,
                "major_subresult_type": "bridge object/tool",
                "major_subresult_assessment": {"score_total": 10, "qualifies": False},
                "rationale": "Worth active depth.",
            },
            {
                "branch_id": "disclayer.demo.family.target-grounding",
                "decision": "freeze",
                "value_score": 0.21,
                "value_band": "low-value",
                "governor_rank": 2,
                "major_subresult_type": "research recommendation",
                "major_subresult_assessment": {"score_total": 1, "qualifies": False},
                "rationale": "Too inert for active depth.",
            },
        ],
        "expert_package_decisions": [],
        "summary": [],
    }
    governor_json, governor_md = discovery_governor_paths(artifacts_dir)
    write_report(governor_report, output_json=governor_json, output_md=governor_md)

    branch_state, execution_index, _paths, outputs = execute_active_discovery_branches(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        limit=2,
    )

    assert len(outputs) == 1
    assert outputs[0]["branch_id"] == "disclayer.demo.family.realization"
    rows = {row["branch_id"]: row for row in branch_state["branches"]}
    assert rows["disclayer.demo.family.realization"]["status"] == "completed"
    assert rows["disclayer.demo.family.target-grounding"]["status"] == "deprioritized"


def test_discovery_governor_reactivates_completed_branch_when_it_remains_top_value(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _write_json(
        artifacts_dir / "discovery-branch-queue.json",
        {
            "metadata": {"kb_ref": "demo"},
            "branches": [
                {
                    "branch_id": "disclayer.demo.family.realization",
                    "status": "completed",
                    "target_label": "Carrier Realization Prompt",
                    "routing_priority": 2.1,
                    "attempt_count": 1,
                    "last_outcome_summary": "Completed one local pass.",
                },
                {
                    "branch_id": "disclayer.demo.family.low-value",
                    "status": "pending",
                    "target_label": "Low-value Prompt",
                    "routing_priority": 0.1,
                    "attempt_count": 0,
                },
            ],
        },
    )
    state = load_discovery_branch_state(artifacts_dir / "discovery-branch-queue.json", kb_ref="demo")
    report = {
        "metadata": {"kb_ref": "demo"},
        "branch_decisions": [
            {
                "branch_id": "disclayer.demo.family.realization",
                "decision": "deepen",
                "value_score": 0.82,
                "value_band": "high-value",
                "governor_rank": 1,
                "major_subresult_type": "bridge object/tool",
                "major_subresult_assessment": {"score_total": 10, "qualifies": False},
                "rationale": "Still the strongest active route.",
                "revisit_penalty": 0.1,
            },
            {
                "branch_id": "disclayer.demo.family.low-value",
                "decision": "freeze",
                "value_score": 0.18,
                "value_band": "low-value",
                "governor_rank": 2,
                "major_subresult_type": "research recommendation",
                "major_subresult_assessment": {"score_total": 2, "qualifies": False},
                "rationale": "Too weak to keep in the active frontier.",
                "revisit_penalty": 0.5,
            },
        ],
    }

    apply_governor_to_branch_state(state, report=report, activate_top_k=1)

    rows = {row["branch_id"]: row for row in state["branches"]}
    assert rows["disclayer.demo.family.realization"]["status"] == "active"
    assert rows["disclayer.demo.family.low-value"]["status"] == "deprioritized"


def test_promoter_filters_expert_packages_with_governor_decisions(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    _write_json(
        artifacts_dir / "expert-conjectures.json",
        {
            "metadata": {"kb_ref": "demo"},
            "agenda": {
                "ready_for_prove": [
                    {
                        "package_id": "conjpkg.demo.01",
                        "branch_id": "disclayer.demo.family.realization",
                        "routing_priority": 3.0,
                        "title": "Witness realization theorem",
                        "exact_statement": "There exists an admissible witness family forcing the target consequence.",
                        "source_statement_id": "st.src",
                        "target_statement_id": "st.tgt",
                        "source_excerpt": "Source excerpt.",
                        "target_excerpt": "Target excerpt.",
                        "route_synopsis": "Realize the witness family.",
                        "linked_queue_ids": ["proofq.demo.001"],
                        "linked_bridge_ids": ["bridge.001"],
                        "restricted_regime_mode": "special-case",
                        "bridge_object": {"name": "Witness family", "kind": "family", "invariant": "witness profile"},
                        "first_nontrivial_lemma": {"title": "Realization lemma", "statement": "For every admissible witness family, the realization preserves the witness profile."},
                        "negative_barrier_version": "No such witness family exists under the current constraints.",
                        "independent_value_claim": "This theorem matters independently of the main conjecture.",
                        "expert_gate": {"passes": True, "score": 6},
                    },
                    {
                        "package_id": "conjpkg.demo.02",
                        "branch_id": "disclayer.demo.family.target-grounding",
                        "routing_priority": 2.0,
                        "title": "Target restatement packet",
                        "exact_statement": "The target theorem is interesting.",
                        "source_statement_id": "st.src",
                        "target_statement_id": "st.tgt.2",
                        "source_excerpt": "Source excerpt.",
                        "target_excerpt": "Target excerpt 2.",
                        "route_synopsis": "Restate the target.",
                        "linked_queue_ids": ["proofq.demo.002"],
                        "linked_bridge_ids": ["bridge.002"],
                        "restricted_regime_mode": "special-case",
                        "bridge_object": {"name": "Target reminder", "kind": "note", "invariant": ""},
                        "first_nontrivial_lemma": {"title": "Reminder", "statement": "If source theorem S holds then target theorem T."},
                        "negative_barrier_version": "No target restatement is decisive.",
                        "independent_value_claim": "This is mostly internal context.",
                        "expert_gate": {"passes": True, "score": 6},
                    },
                ]
            },
        },
    )
    _write_json(artifacts_dir / "discovery-branch-synthesis.json", {"metadata": {"kb_ref": "demo"}, "agenda": {"ready_for_prove": []}})
    governor_report = {
        "metadata": {"kb_ref": "demo"},
        "branch_decisions": [],
        "expert_package_decisions": [
            {
                "package_id": "conjpkg.demo.01",
                "decision": "queue_for_proof",
                "value_score": 0.81,
                "value_band": "high-value",
                "rationale": "Proof-worthy.",
                "major_subresult_assessment": {"score_total": 10, "qualifies": False},
            },
            {
                "package_id": "conjpkg.demo.02",
                "decision": "freeze",
                "value_score": 0.28,
                "value_band": "low-value",
                "rationale": "Elegant but inert.",
                "major_subresult_assessment": {"score_total": 2, "qualifies": False},
            },
        ],
        "summary": [],
    }
    governor_json, governor_md = discovery_governor_paths(artifacts_dir)
    write_report(governor_report, output_json=governor_json, output_md=governor_md)

    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo")

    assert report["metadata"]["programme_count"] == 1
    assert report["metadata"]["suppressed_by_governor"] == 1
    promoted = report["entries"][0]
    assert promoted["theorem_package_id"] == "conjpkg.demo.01"
    assert promoted["governor_decision"] == "queue_for_proof"
    assert promoted["governor_rationale"] == "Proof-worthy."
