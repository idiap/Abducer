# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for executing active routed discovery branches."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
DISCOVERY_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-discovery-cycle" / "scripts"
PROFILE_SCRIPT_DIR = ROOT / "skills" / "evaluation" / "kb-discovery-breakthrough-profiler" / "scripts"

for path in (COMMON_DIR, DISCOVERY_SCRIPT_DIR, PROFILE_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from execute_discovery_branches import discovery_execution_paths, execute_active_discovery_branches
from agentic.discovery.contracts import ContractError, canonical_digest
from generate_discovery_breakthrough_profile import build_discovery_pattern_routing, build_expanded_prompt_pack, spawn_discovery_branches
from problem_mathlib import default_mathlib, mathlib_paths, save_mathlib_index
from proof_queue import default_queue, enqueue_entries, proof_queue_paths, save_proof_queue


def _profile_report() -> dict:
    return {
        "metadata": {"kb_ref": "demo"},
        "profiles": [
            {
                "obstruction_class": "carrier-realization",
                "breakthrough_family": "realization",
                "required_move": "Realize an explicit carrier.",
                "abstraction_required": "A witness family with admissibility conditions.",
                "minimal_theorem_shape": "If source theorem S holds, construct a carrier C forcing target theorem T.",
                "major_subresult_type": "bridge object/tool",
                "search_modes": ["explicit carrier construction"],
                "anti_patterns": ["renaming the carrier"],
                "queue_ids": ["proofq.demo.001", "proofq.demo.002"],
                "reference_ids": ["mathlibref.demo.001"],
                "effect_notes": ["Target already grounded."],
                "pressure_score": 1.0,
                "top_priority": 0.9,
                "sample_theorem_targets": ["Construct a route-specific witness carrier."],
            },
            {
                "obstruction_class": "target-alignment",
                "breakthrough_family": "alignment",
                "required_move": "Identify the target object-class correspondence.",
                "abstraction_required": "A correspondence theorem between the local carrier and target-side object class.",
                "minimal_theorem_shape": "Every local carrier C induces a target object D preserving the route invariant.",
                "major_subresult_type": "transfer principle",
                "search_modes": ["object-class correspondence", "transport"],
                "anti_patterns": ["topical similarity as equivalence"],
                "queue_ids": ["proofq.demo.001", "proofq.demo.002"],
                "reference_ids": ["mathlibref.demo.002"],
                "effect_notes": ["The route is blocked by missing correspondence."],
                "pressure_score": 0.8,
                "top_priority": 0.7,
                "sample_theorem_targets": ["Construct D from C."],
            },
        ],
    }


@pytest.mark.expensive
def test_discovery_branch_executor_materializes_execution_reports(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Primary route conjecture",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "Primary route conjecture.",
                "conjecture_statement": "Construct an admissible witness family.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "A barely nontrivial lower bound for MCSP.",
                "target_excerpt": "Major consequences such as NP not in P/poly.",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Prove the witness family transfers the lower bound.",
                "status": "blocked",
            },
            {
                "queue_key": "bridge.002|st.tgt.2|route-conjecture",
                "title": "Secondary route conjecture",
                "priority": 0.84,
                "bridge_id": "bridge.002",
                "claim_type": "route-conjecture",
                "claim_text": "Secondary route conjecture.",
                "conjecture_statement": "Construct a transport law for the witness family.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.2",
                "source_excerpt": "A barely nontrivial lower bound for MCSP.",
                "target_excerpt": "A formula-size lower-bound consequence.",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Prove the transport law preserves the invariant.",
                "status": "blocked",
            },
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    mathlib = default_mathlib(kb_ref="demo")
    mathlib_json, mathlib_md = mathlib_paths(repo_root, "demo")
    save_mathlib_index(mathlib, json_path=mathlib_json, md_path=mathlib_md)

    report = _profile_report()
    prompt_pack = build_expanded_prompt_pack(report)
    routing = build_discovery_pattern_routing(report, prompt_pack)
    spawn_discovery_branches(routing, artifacts_dir=artifacts_dir, activate_top_k=7)

    branch_state, execution_index, execution_paths, outputs = execute_active_discovery_branches(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        limit=7,
    )

    assert execution_paths == discovery_execution_paths(artifacts_dir)
    assert execution_paths[0].exists()
    assert execution_paths[1].exists()
    assert len(outputs) == 7
    assert execution_index["metadata"]["execution_count"] == 7
    assert any(row["attempt_count"] == 1 for row in branch_state["branches"])
    assert any(Path(row["md"]).exists() for row in outputs)
    first_report = Path(outputs[0]["md"]).read_text(encoding="utf-8")
    execution_reports = [json.loads(Path(row["json"]).read_text(encoding="utf-8")) for row in outputs]
    assert any(report["metadata"]["status"] == "completed-state-delta" for report in execution_reports)
    assert any(report["execution"]["state_delta"]["has_state_delta"] is True for report in execution_reports)
    assert any(report["execution"]["state_delta"]["promotable_theorem_count"] >= 1 for report in execution_reports)
    assert all(report["execution"]["mathematical_packet_contract"]["required"] is True for report in execution_reports)
    assert any(report["execution"]["lean_symbolic_search"]["available"] is True for report in execution_reports)
    assert any(report["execution"]["lean_symbolic_search"]["build_ok"] is True for report in execution_reports)
    assert any(Path(report["execution"]["lean_symbolic_search"]["module_path"]).exists() for report in execution_reports)
    assert "## Candidate Claims" in first_report
    assert "## Lean Search" in first_report
    assert "## Native Mathematical Packet Contract" in first_report
    assert "## External Framework Search Gate" in first_report
    assert "Construct a route-specific witness carrier." in first_report
    assert any("## State Delta" in Path(row["md"]).read_text(encoding="utf-8") for row in outputs)
    assert any("## Theorem Candidates" in Path(row["md"]).read_text(encoding="utf-8") for row in outputs)
    assert any("Promotable theorem candidates:" in Path(row["md"]).read_text(encoding="utf-8") for row in outputs)
    assert any(
        "Routing heuristic: recommended=True" in Path(row["md"]).read_text(encoding="utf-8")
        and "Active criteria:" in Path(row["md"]).read_text(encoding="utf-8")
        for row in outputs
    )

    _branch_state_2, execution_index_2, _execution_paths_2, outputs_2 = execute_active_discovery_branches(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        limit=7,
    )
    _branch_state_3, execution_index_3, _execution_paths_3, outputs_3 = execute_active_discovery_branches(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        limit=7,
    )

    assert len(outputs_2) >= 1
    assert outputs_3 == []
    assert execution_index_3["metadata"]["execution_count"] == execution_index_2["metadata"]["execution_count"]
    assert execution_index_3["metadata"]["last_run_execution_count"] == 0
    assert execution_index_3["metadata"]["last_run_lean_route_count"] == 0
    assert execution_index_3["metadata"]["last_run_lean_candidate_count"] == 0


def test_discovery_branch_executor_honors_exact_id_and_row_digest(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    prompt_pack = build_expanded_prompt_pack(_profile_report())
    routing = build_discovery_pattern_routing(_profile_report(), prompt_pack)
    state, _paths, _dossiers = spawn_discovery_branches(
        routing,
        artifacts_dir=artifacts_dir,
        activate_top_k=7,
    )
    selected = state["branches"][-1]
    selected_id = selected["branch_id"]
    selected_digest = canonical_digest(selected)

    with pytest.raises(ContractError, match="changed after binding preflight"):
        execute_active_discovery_branches(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref="demo",
            limit=7,
            exact_branch_id=selected_id,
            expected_branch_digest=canonical_digest({"wrong": True}),
        )

    _branch_state, _index, _execution_paths, outputs = execute_active_discovery_branches(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        limit=7,
        exact_branch_id=selected_id,
        expected_branch_digest=selected_digest,
    )

    assert [row["branch_id"] for row in outputs] == [selected_id]
