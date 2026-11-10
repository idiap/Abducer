# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for promoting theorem-shaped discovery programmes into the proof queue."""

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

from enqueue_discovery_programmes import build_promotions
from enqueue_discovery_programmes import apply_promotions
from proof_queue import default_queue, enqueue_entries, load_proof_queue, proof_queue_paths, save_proof_queue


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def test_promoter_builds_branch_programmes_from_ready_for_prove(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.016|st.tgt|route-conjecture",
                "title": "Existing blocked route",
                "priority": 0.7,
                "bridge_id": "bridge.016",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Existing route conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "MCSP obstruction family",
                "preserved_invariant": "witness complexity",
                "source_excerpt": "Source excerpt.",
                "target_excerpt": "Target excerpt.",
                "status": "blocked",
            }
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    execution_report_path = artifacts_dir / "discovery-branch-executions" / "alignment.json"
    _write_json(
        execution_report_path,
        {
            "metadata": {
                "branch_id": "disclayer.demo.family.alignment",
                "status": "completed-state-delta",
            },
            "execution": {
                "theorem_candidates": [
                    {
                        "title": "Alignment theorem for the witness carrier",
                        "statement": "Every admissible MCSP obstruction family induces a target-side object preserving witness complexity strongly enough to force the target theorem excerpt.",
                        "motivation": "Identify the missing correspondence theorem.",
                        "candidate_object": "MCSP obstruction family",
                        "invariant": "witness complexity",
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
        artifacts_dir / "discovery-branch-synthesis.json",
        {
            "metadata": {"kb_ref": "demo"},
            "agenda": {
                "ready_for_prove": [
                    {
                        "branch_id": "disclayer.demo.family.alignment",
                        "target_label": "Alignment Theorem Prompt",
                        "routing_priority": 2.2,
                        "headline": "Every admissible carrier C induces an object D in the target class.",
                        "rationale": "Identify the missing correspondence theorem.",
                        "artifact_json": str(execution_report_path),
                    }
                ]
            },
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-queue.json",
        {
            "metadata": {"kb_ref": "demo"},
            "branches": [
                {
                    "branch_id": "disclayer.demo.family.alignment",
                    "linked_queue_ids": ["proofq.demo.001"],
                }
            ],
        },
    )

    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo")

    assert report["metadata"]["programme_count"] == 1
    promoted = report["entries"][0]
    assert promoted["claim_type"] == "branch-programme"
    assert promoted["bridge_id"] == "disclayer.demo.family.alignment"
    assert promoted["candidate_object"] == "MCSP obstruction family"
    assert promoted["preserved_invariant"] == "witness complexity"
    assert promoted["source_excerpt"] == "Source excerpt."
    assert promoted["target_excerpt"] == "Target excerpt."
    assert promoted["linked_queue_ids"] == ["proofq.demo.001"]
    assert promoted["missing_route_lemma"] == "Alignment theorem for the witness carrier"
    assert promoted["concretization_status"] == "concrete"
    assert promoted["concretization_score"] == 5
    assert "Every admissible MCSP obstruction family induces a target-side object" in promoted["conjecture_statement"]


def test_promoter_reencodes_schematic_branch_programme_fields_from_local_context(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.020|st.tgt|route-conjecture",
                "title": "Existing blocked route",
                "priority": 0.73,
                "bridge_id": "bridge.020",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Existing route conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "MCSP witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness complexity profile",
                "proof_strategy_family": "transport",
                "negative_route": "Assume no witness family realizes the target-side object.",
                "proof_obligations": ["Build the witness family from the source theorem."],
                "candidate_lemmas": ["Witness-family transport lemma."],
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "status": "blocked",
            }
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    execution_report_path = artifacts_dir / "discovery-branch-executions" / "realization.json"
    _write_json(
        execution_report_path,
        {
            "metadata": {
                "branch_id": "disclayer.demo.family.realization",
                "status": "completed-state-delta",
            },
            "execution": {
                "theorem_candidates": [
                    {
                        "title": "If source theorem S holds in regime R, then carrier C yields target theorem T.",
                        "statement": "There exists an admissible MCSP witness family whose realization map preserves the witness complexity profile and activates the target theorem excerpt.",
                        "motivation": "Target theorem T is fixed. The real theorem under search is the local activation theorem A.",
                        "candidate_object": "MCSP witness family",
                        "invariant": "witness complexity profile",
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
        artifacts_dir / "discovery-branch-synthesis.json",
        {
            "metadata": {"kb_ref": "demo"},
            "agenda": {
                "ready_for_prove": [
                    {
                        "branch_id": "disclayer.demo.family.realization",
                        "target_label": "Carrier Realization Prompt",
                        "routing_priority": 2.2,
                        "headline": "If source theorem S holds in regime R, then carrier C yields target theorem T.",
                        "rationale": "Turn the local carrier into an explicit theorem packet.",
                        "artifact_json": str(execution_report_path),
                    }
                ]
            },
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-queue.json",
        {
            "metadata": {"kb_ref": "demo"},
            "branches": [
                {
                    "branch_id": "disclayer.demo.family.realization",
                    "linked_queue_ids": ["proofq.demo.001"],
                }
            ],
        },
    )

    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo")
    promoted = report["entries"][0]

    assert promoted["title"] == "Carrier Realization Prompt: Carrier Realization theorem for MCSP witness family"
    assert promoted["missing_route_lemma"] == "Carrier Realization theorem for MCSP witness family"
    assert promoted["route_synopsis"].startswith("Start from `st.src` with source content `Source theorem excerpt.`")
    assert promoted["proof_strategy_family"] == "transport"
    assert promoted["negative_route"] == "Assume no witness family realizes the target-side object."
    assert promoted["proof_obligations"] == ["Build the witness family from the source theorem."]


def test_apply_promotions_reopens_blocked_expert_conjecture_as_pending(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "disclayer.demo.family.realization|st.tgt|expert-conjecture-conjpkg.demo.001",
                "title": "Old blocked expert packet",
                "priority": 0.91,
                "bridge_id": "disclayer.demo.family.realization",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible witness family realizing the target theorem.",
                "conjecture_statement": "There exists an admissible witness family realizing the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source lower-bound excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Witness realization lemma",
                "theorem_package_id": "conjpkg.demo.001",
                "status": "blocked",
                "final_attempt_id": "attempt.demo.001",
                "result_id": "mathlibneg.demo.001",
                "resolution_summary": "Old blocked outcome.",
            }
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    _write_json(
        artifacts_dir / "expert-conjectures.json",
        {
            "metadata": {"kb_ref": "demo"},
            "agenda": {
                "ready_for_prove": [
                    {
                        "package_id": "conjpkg.demo.001",
                        "title": "Witness realization packet",
                        "branch_id": "disclayer.demo.family.realization",
                        "exact_statement": "For every admissible witness family, the realization map preserves the witness complexity profile and reaches the target theorem.",
                        "source_statement_id": "st.src",
                        "target_statement_id": "st.tgt",
                        "source_excerpt": "Source lower-bound excerpt.",
                        "target_excerpt": "Target theorem excerpt.",
                        "route_synopsis": "Transport the source lower bound through an admissible witness family.",
                        "bridge_object": {
                            "name": "Witness family",
                            "kind": "family of witness instances",
                            "definition": "An admissible family indexed by the source theorem.",
                            "invariant": "witness complexity profile",
                        },
                        "first_nontrivial_lemma": {
                            "title": "Witness realization lemma",
                            "statement": "The admissible witness family realizes the target theorem.",
                        },
                        "restricted_regime_mode": "transport",
                        "admissibility_conditions": ["The witness family is admissible."],
                        "negative_barrier_version": "Assume no admissible witness family realizes the target theorem.",
                        "expert_gate": {"passes": True, "score": 6},
                    }
                ]
            },
        },
    )

    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo")
    promoted = report["entries"][0]
    assert promoted["proof_strategy_family"] == "transport"
    assert promoted["negative_route"].startswith("Assume")
    assert promoted["failure_diagnosis"].startswith("The route fails if")
    assert promoted["proof_obligations"] == ["The admissible witness family realizes the target theorem."]
    assert promoted["candidate_lemmas"] == ["Witness realization lemma"]
    _queue, added, updated, _deferred, _queue_paths = apply_promotions(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        report=report,
    )

    refreshed = load_proof_queue(queue_json, kb_ref="demo")
    promoted = next(row for row in refreshed["entries"] if row.get("theorem_package_id") == "conjpkg.demo.001")

    assert added == 0
    assert updated == 1
    assert refreshed["metadata"]["pending_count"] >= 1
    assert promoted["status"] == "pending"
    assert promoted["final_attempt_id"] == ""
    assert promoted["result_id"] == ""
    assert promoted["resolution_summary"] == ""
    assert promoted["interpretability_contract"]["warnings"] == []
    assert promoted["inference_diagnosis"]["context_status"] == "well-posed"


def test_promoter_skips_branch_programmes_without_concrete_theorem_candidate(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.010|st.tgt|route-conjecture",
                "title": "Transport route",
                "priority": 0.6,
                "bridge_id": "bridge.010",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Transport route conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "status": "blocked",
            }
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    execution_report_path = artifacts_dir / "discovery-branch-executions" / "transport.json"
    _write_json(
        execution_report_path,
        {
            "metadata": {
                "branch_id": "disclayer.demo.family.transport",
                "status": "completed-analysis-pass",
            },
            "execution": {
                "theorem_candidates": [
                    {
                        "title": "Transport theorem placeholder",
                        "statement": "If source theorem S holds in regime R, carrier C yields target theorem T.",
                        "concretization_status": "partial",
                        "concretization_score": 1,
                    }
                ],
                "state_delta": {
                    "delta_kind": "analysis-only",
                    "promotable_theorem_count": 0,
                    "max_concretization_score": 1,
                },
            },
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-synthesis.json",
        {
            "metadata": {"kb_ref": "demo"},
            "agenda": {
                "ready_for_prove": [
                    {
                        "branch_id": "disclayer.demo.family.transport",
                        "target_label": "Transport Prompt",
                        "routing_priority": 1.2,
                        "headline": "If source theorem S holds in regime R, carrier C yields target theorem T.",
                        "rationale": "Still schematic.",
                        "artifact_json": str(execution_report_path),
                    }
                ]
            },
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-queue.json",
        {
            "metadata": {"kb_ref": "demo"},
            "branches": [
                {
                    "branch_id": "disclayer.demo.family.transport",
                    "linked_queue_ids": ["proofq.demo.001"],
                }
            ],
        },
    )

    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo")
    assert report["metadata"]["programme_count"] == 0
    assert report["entries"] == []


def test_promoter_prefers_expert_conjectures_when_present(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Blocked route",
                "priority": 0.9,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Blocked route.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source excerpt.",
                "target_excerpt": "Target excerpt.",
                "status": "blocked",
            }
        ],
    )
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
                        "title": "Carrier realization theorem",
                        "exact_statement": "There exists an admissible MCSP obstruction family forcing the target consequence.",
                        "source_statement_id": "st.src",
                        "target_statement_id": "st.tgt",
                        "source_excerpt": "Source excerpt.",
                        "target_excerpt": "Target excerpt.",
                        "route_synopsis": "Realize the carrier.",
                        "linked_queue_ids": ["proofq.demo.001"],
                        "linked_bridge_ids": ["bridge.001"],
                        "restricted_regime_mode": "special-case",
                        "bridge_object": {
                            "name": "MCSP obstruction family",
                            "kind": "family of obstruction instances",
                            "invariant": "witness complexity profile",
                        },
                        "first_nontrivial_lemma": {
                            "title": "Carrier realization lemma",
                            "statement": "For every admissible MCSP obstruction family, the first realization step preserves the witness complexity profile.",
                        },
                        "expert_gate": {"passes": True, "score": 6},
                    }
                ]
            },
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-synthesis.json",
        {
            "metadata": {"kb_ref": "demo"},
            "agenda": {"ready_for_prove": []},
        },
    )

    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo")

    assert report["metadata"]["source"] == "expert-conjectures"
    assert report["metadata"]["programme_count"] == 1
    promoted = report["entries"][0]
    assert promoted["claim_type"] == "expert-conjecture"
    assert promoted["bridge_id"] == "bridge.001"
    assert promoted["candidate_object"] == "MCSP obstruction family"
    assert promoted["bridge_object_definition"] == ""
    assert promoted["restricted_regime_mode"] == "special-case"
    assert promoted["theorem_package_id"] == "conjpkg.demo.01"


def test_promoter_keeps_distinct_expert_packages_with_shared_branch_and_object(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt.1|route-conjecture",
                "title": "Blocked route 1",
                "priority": 0.9,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Blocked route 1.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.1",
                "status": "blocked",
            }
        ],
    )
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
                        "title": "Carrier realization theorem A",
                        "exact_statement": "There exists an admissible MCSP obstruction family forcing target A.",
                        "source_statement_id": "st.src",
                        "target_statement_id": "st.tgt.1",
                        "source_excerpt": "Source excerpt.",
                        "target_excerpt": "Target excerpt A.",
                        "route_synopsis": "Realize the carrier for target A.",
                        "linked_queue_ids": ["proofq.demo.001"],
                        "linked_bridge_ids": ["bridge.001", "bridge.002"],
                        "restricted_regime_mode": "special-case",
                        "bridge_object": {
                            "name": "MCSP obstruction family",
                            "kind": "family of obstruction instances",
                            "invariant": "witness complexity profile",
                        },
                        "first_nontrivial_lemma": {
                            "title": "Carrier realization lemma A",
                            "statement": "Carrier realization statement A.",
                        },
                        "expert_gate": {"passes": True, "score": 6},
                    },
                    {
                        "package_id": "conjpkg.demo.02",
                        "branch_id": "disclayer.demo.family.realization",
                        "routing_priority": 2.9,
                        "title": "Carrier realization theorem B",
                        "exact_statement": "There exists an admissible MCSP obstruction family forcing target B.",
                        "source_statement_id": "st.src",
                        "target_statement_id": "st.tgt.2",
                        "source_excerpt": "Source excerpt.",
                        "target_excerpt": "Target excerpt B.",
                        "route_synopsis": "Realize the carrier for target B.",
                        "linked_queue_ids": ["proofq.demo.001"],
                        "linked_bridge_ids": ["bridge.001", "bridge.002"],
                        "restricted_regime_mode": "threshold-version",
                        "bridge_object": {
                            "name": "MCSP obstruction family",
                            "kind": "family of obstruction instances",
                            "invariant": "witness complexity profile",
                        },
                        "first_nontrivial_lemma": {
                            "title": "Carrier realization lemma B",
                            "statement": "Carrier realization statement B.",
                        },
                        "expert_gate": {"passes": True, "score": 6},
                    },
                ]
            },
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-synthesis.json",
        {
            "metadata": {"kb_ref": "demo"},
            "agenda": {"ready_for_prove": []},
        },
    )

    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo")
    queue, added, updated, deferred, _ = apply_promotions(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        report=report,
    )

    expert_entries = [row for row in queue["entries"] if row.get("claim_type") == "expert-conjecture"]
    assert added == 2
    assert updated == 0
    assert deferred == 0
    assert len(expert_entries) == 2
    assert {row["theorem_package_id"] for row in expert_entries} == {"conjpkg.demo.01", "conjpkg.demo.02"}


def test_promoter_preserves_expert_theorem_package_fields(tmp_path: Path) -> None:
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
                        "package_id": "conjpkg.demo.03",
                        "branch_id": "disclayer.demo.family.transport",
                        "routing_priority": 2.5,
                        "title": "Transport theorem",
                        "exact_statement": "Every admissible obstruction family transports to the target regime.",
                        "source_statement_id": "st.src",
                        "target_statement_id": "st.tgt",
                        "source_excerpt": "Source excerpt.",
                        "target_excerpt": "Target excerpt.",
                        "route_synopsis": "Transport the carrier.",
                        "linked_queue_ids": [],
                        "linked_bridge_ids": ["bridge.010"],
                        "restricted_regime_mode": "transport-lemma",
                        "bridge_object": {
                            "name": "MCSP obstruction family",
                            "kind": "family of obstruction instances",
                            "definition": "A typed family of obstruction instances mediating the source and target regimes.",
                            "invariant": "witness complexity profile",
                        },
                        "admissibility_conditions": [
                            "The family is explicitly defined.",
                            "The family preserves the witness profile.",
                        ],
                        "first_nontrivial_lemma": {
                            "title": "Transport lemma",
                            "statement": "The obstruction family transports the witness profile to the target regime.",
                        },
                        "negative_barrier_version": "No such transport exists without extra structure.",
                        "independent_value_claim": "This transport theorem matters independently of the main conjecture.",
                        "regime_and_quantifiers": {
                            "quantifier_frame": "For every admissible obstruction family in the transport regime.",
                        },
                        "branch_to_definition": {"transport_laws": ["Transport law A."]},
                        "foundation_search": {
                            "recommended": True,
                            "mode": "targeted-foundation-search",
                            "candidate_framework_regions": ["transport framework"],
                        },
                        "expert_gate": {"passes": True, "score": 6},
                    }
                ]
            },
        },
    )
    _write_json(
        artifacts_dir / "discovery-branch-synthesis.json",
        {"metadata": {"kb_ref": "demo"}, "agenda": {"ready_for_prove": []}},
    )

    report = build_promotions(repo_root=repo_root, artifacts_dir=artifacts_dir, kb_ref="demo")
    promoted = report["entries"][0]

    assert promoted["bridge_object_definition"] == "A typed family of obstruction instances mediating the source and target regimes."
    assert promoted["first_nontrivial_lemma_title"] == "Transport lemma"
    assert promoted["first_nontrivial_lemma_statement"] == "The obstruction family transports the witness profile to the target regime."
    assert promoted["negative_barrier_version"] == "No such transport exists without extra structure."
    assert promoted["independent_value_claim"] == "This transport theorem matters independently of the main conjecture."
    assert promoted["regime_and_quantifiers"]["quantifier_frame"] == "For every admissible obstruction family in the transport regime."
    assert promoted["mathematical_layers"]["latex"]["theorem_statement"].startswith(r"\forall W")
    assert "theorem transport_theorem" in promoted["mathematical_layers"]["lean_style"]["scaffold"]


def test_apply_promotions_retires_stale_discovery_packets_from_active_frontier(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "disclayer.demo.family.transport|st.tgt|branch-programme-transport",
                "title": "Transport Prompt: If source theorem S holds in regime R, carrier C yields target theorem T.",
                "priority": 2.1,
                "bridge_id": "disclayer.demo.family.transport",
                "claim_type": "branch-programme",
                "claim_text": "If source theorem S holds in regime R, carrier C yields target theorem T.",
                "conjecture_statement": "If source theorem S holds in regime R, carrier C yields target theorem T.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source excerpt.",
                "target_excerpt": "Target excerpt.",
                "route_synopsis": "Move from source theorem S toward target theorem T through carrier C...",
                "candidate_object": "unspecified witness family",
                "missing_route_lemma": "If source theorem S holds in regime R, carrier C yields target theorem T.",
                "discovery_branch_id": "disclayer.demo.family.transport",
            }
        ],
    )
    stale = queue["entries"][0]
    stale["status"] = "deferred"
    stale["deferred_by"] = "llm-interpretability-gate"
    stale["deferred_reason"] = "Defer until re-encoded."
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    report = {
        "metadata": {"kb_ref": "demo", "programme_count": 1, "source": "expert-conjectures"},
        "entries": [
            {
                "queue_key": "bridge.001|st.tgt.2|expert-conjecture-demo",
                "title": "Witness-family transport theorem",
                "priority": 1.7,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.2",
                "source_excerpt": "Source excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Move from st.src to st.tgt.2 through a Witness family.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness complexity profile",
                "proof_strategy_family": "transport",
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "proof_obligations": ["Show the witness family preserves the invariant."],
                "discovery_branch_id": "disclayer.demo.family.equivalence-coherence-reframing",
            }
        ],
    }

    queue, added, updated, deferred, _ = apply_promotions(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        report=report,
    )

    stale = next(row for row in queue["entries"] if row["claim_type"] == "branch-programme")
    assert added == 1
    assert updated == 0
    assert deferred == 1
    assert stale["status"] == "deferred"
    assert stale["retired_from_active_frontier"] is True
    assert stale["deferred_by"] == "inactive-discovery-frontier"
    assert "Retired because an expert-grade discovery packet now carries the active prove frontier." in stale["deferred_reason"]
