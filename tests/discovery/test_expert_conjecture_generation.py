# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for compiling discovery branches into expert conjecture packages."""

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

from generate_expert_conjectures import build_report
from proof_queue import default_queue, enqueue_entries, proof_queue_paths, save_proof_queue


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def test_expert_conjecture_report_emits_theorem_packages_and_restricted_programmes(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    executions_dir = artifacts_dir / "discovery-branch-executions"
    executions_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Primary blocked route",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Construct an admissible MCSP obstruction family forcing the target consequence.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "A barely nontrivial lower bound for MCSP in a weak model.",
                "target_excerpt": "Major consequences such as NP not in P/poly.",
                "candidate_object": "MCSP obstruction family",
                "carrier_kind": "family of obstruction instances",
                "preserved_invariant": "witness complexity profile",
                "route_synopsis": "Move from a weak lower bound into a target-side magnification consequence.",
                "missing_route_lemma": "Realize the obstruction family and preserve the invariant.",
                "status": "blocked",
            }
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    execution_report_path = executions_dir / "realization.json"
    _write_json(
        execution_report_path,
        {
            "metadata": {
                "execution_id": "discexec.demo.001",
                "branch_id": "disclayer.demo.family.realization",
                "status": "completed-state-delta",
            },
            "branch": {
                "branch_id": "disclayer.demo.family.realization",
                "target_id": "realization",
                "target_label": "Realization Prompt",
                "routing_priority": 2.5,
                "required_move": "Realize the obstruction family explicitly.",
                "linked_queue_ids": ["proofq.demo.001"],
            },
            "execution": {
                "theorem_candidates": [
                    {
                        "title": "Carrier realization theorem",
                        "statement": "There exists an admissible MCSP obstruction family such that the weak-model MCSP lower bound is organized into a route preserving witness complexity and thereby supports major consequences such as NP not in P/poly.",
                        "candidate_object": "MCSP obstruction family",
                        "invariant": "witness complexity profile",
                        "concretization_status": "concrete",
                        "concretization_score": 5,
                    }
                ],
                "concept_revisions": [
                    {
                        "label": "realization-special-case",
                        "revision": "First prove the carrier realization theorem in the near-threshold regime.",
                        "epistemic_gain": "Localizes the first theorem that would make the route concrete.",
                    }
                ],
                "negative_outputs": ["no admissible carrier exists unless the witness profile is sharpened"],
                "external_framework_search": {
                    "recommended": True,
                    "mode": "targeted-foundation-search",
                    "candidate_framework_regions": ["obstruction family framework"],
                    "local_prerequisites": ["Record the exact failure of the current carrier realization."],
                    "query_templates": ["obstruction family framework preserving witness complexity"],
                },
                "lens_artifacts": {
                    "transport_obligations": ["Transport the witness profile through the realization map."],
                    "equivalence_claims": ["The obstruction family should match the target-side carrier."],
                    "coherence_failures": ["The current carrier lacks a coherence witness."],
                },
            },
        },
    )
    _write_json(
        executions_dir / "index.json",
        {
            "metadata": {"kb_ref": "demo", "execution_count": 1},
            "executions": [
                {
                    "execution_id": "discexec.demo.001",
                    "branch_id": "disclayer.demo.family.realization",
                    "artifact_json": str(execution_report_path),
                    "artifact_md": str(executions_dir / "realization.md"),
                }
            ],
        },
    )

    report = build_report(artifacts_dir=artifacts_dir, kb_ref="demo", repo_root=repo_root)

    assert report["metadata"]["expert_conjecture_count"] == 1
    assert report["metadata"]["ready_for_prove_count"] == 1
    assert report["metadata"]["restricted_regime_count"] == 1
    package = report["expert_conjectures"][0]
    assert package["restricted_regime_mode"] == "special-case"
    assert package["bridge_object"]["name"] == "MCSP obstruction family"
    assert "weak-model MCSP lower bound" in package["exact_statement"]
    assert package["expert_gate"]["passes"] is True
    assert package["branch_to_definition"]["equivalence_claims"] == [
        "The obstruction family should match the target-side carrier."
    ]
    assert package["proof_strategy_family"] == "constructive-realization"
    assert package["negative_route"].startswith("Assume `MCSP obstruction family` cannot be realized")
    assert package["failure_diagnosis"].startswith("The route fails if `MCSP obstruction family` cannot be realized")
    assert package["proof_obligations"]
    assert "first route-specific realization step preserves" in package["proof_obligations"][0]
    assert package["candidate_lemmas"][0] == "Carrier realization theorem"
    assert package["foundation_search"]["recommended"] is True
    assert package["mathematical_layers"]["latex"]["theorem_statement"].startswith(r"\forall W")
    assert "constant BridgeWitness" in package["mathematical_layers"]["lean_style"]["scaffold"]
    assert report["restricted_regime_programmes"][0]["title"].startswith("Special-Case Theorem")


def test_expert_conjecture_report_reencodes_truncated_route_synopsis_from_queue_context(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    executions_dir = artifacts_dir / "discovery-branch-executions"
    executions_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Primary blocked route",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Construct an admissible MCSP witness family forcing the target consequence.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "A barely nontrivial lower bound for MCSP in a weak model.",
                "target_excerpt": "Major lower bounds for NP in a stronger model.",
                "candidate_object": "MCSP witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness complexity profile",
                "route_synopsis": "Move from st.src toward st.tgt to obtain major lower bounds for NP in a stronger model...",
                "missing_route_lemma": "Realize the witness family and preserve the invariant.",
                "status": "blocked",
            }
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    execution_report_path = executions_dir / "equivalence.json"
    _write_json(
        execution_report_path,
        {
            "metadata": {
                "execution_id": "discexec.demo.001",
                "branch_id": "disclayer.demo.family.equivalence",
                "status": "completed-state-delta",
            },
            "branch": {
                "branch_id": "disclayer.demo.family.equivalence",
                "target_id": "equivalence-coherence-reframing",
                "target_label": "Equivalence Prompt",
                "routing_priority": 2.5,
                "required_move": "Recast the blocked frontier as an equivalence problem.",
                "linked_queue_ids": ["proofq.demo.001"],
            },
            "execution": {
                "theorem_candidates": [
                    {
                        "title": "Equivalence and coherent transport theorem",
                        "statement": "There exists an equivalence witness for the MCSP witness family that transports the witness complexity profile to the stronger target theorem.",
                        "candidate_object": "MCSP witness family",
                        "invariant": "witness complexity profile",
                        "concretization_status": "concrete",
                        "concretization_score": 6,
                    }
                ],
                "concept_revisions": [],
                "negative_outputs": ["no equivalence witness exists without a transport law"],
                "lens_artifacts": {},
            },
        },
    )
    _write_json(
        executions_dir / "index.json",
        {
            "metadata": {"kb_ref": "demo", "execution_count": 1},
            "executions": [
                {
                    "execution_id": "discexec.demo.001",
                    "branch_id": "disclayer.demo.family.equivalence",
                    "artifact_json": str(execution_report_path),
                    "artifact_md": str(executions_dir / "equivalence.md"),
                }
            ],
        },
    )

    report = build_report(artifacts_dir=artifacts_dir, kb_ref="demo", repo_root=repo_root)

    package = report["expert_conjectures"][0]
    assert "..." not in package["route_synopsis"]
    assert "Major lower bounds for NP in a stronger model." in package["route_synopsis"]
    assert package["mathematical_layers"]["quantifier_signature"].startswith("For every admissible")


def test_expert_conjecture_report_preserves_prompt_native_mathematical_layers(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    executions_dir = artifacts_dir / "discovery-branch-executions"
    executions_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Primary blocked route",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "conjecture_statement": "Construct an admissible MCSP witness family forcing the target consequence.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "candidate_object": "MCSP witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness complexity profile",
                "route_synopsis": "Move from st.src toward st.tgt through a witness family.",
                "missing_route_lemma": "Witness-family transport lemma.",
                "status": "blocked",
            }
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)

    execution_report_path = executions_dir / "equivalence.json"
    native_layers = {
        "quantifier_signature": "For every admissible MCSP witness family W in the local route.",
        "object_signature": {"bridge_object": "MCSP witness family"},
        "symbol_ledger": [{"symbol": "W", "meaning": "an admissible witness family"}],
        "latex": {"theorem_statement": r"\forall W,\ \mathrm{Adm}(W) \to \exists w,\ \mathrm{Good}(W,w)."},
        "lean_style": {
            "status": "non-executable-scaffold",
            "theorem_name": "native_transport_packet",
            "scaffold": "theorem native_transport_packet : True := by\n  trivial",
        },
    }
    _write_json(
        execution_report_path,
        {
            "metadata": {
                "execution_id": "discexec.demo.001",
                "branch_id": "disclayer.demo.family.equivalence",
                "status": "completed-state-delta",
            },
            "branch": {
                "branch_id": "disclayer.demo.family.equivalence",
                "target_id": "equivalence-coherence-reframing",
                "target_label": "Equivalence Prompt",
                "routing_priority": 2.5,
                "required_move": "Recast the blocked frontier as an equivalence problem.",
                "linked_queue_ids": ["proofq.demo.001"],
            },
            "execution": {
                "theorem_candidates": [
                    {
                        "title": "Equivalence and coherent transport theorem",
                        "statement": "There exists an equivalence witness for the MCSP witness family that transports the witness complexity profile to the stronger target theorem.",
                        "candidate_object": "MCSP witness family",
                        "invariant": "witness complexity profile",
                        "concretization_status": "concrete",
                        "concretization_score": 6,
                        "mathematical_layers": native_layers,
                    }
                ],
                "concept_revisions": [],
                "negative_outputs": ["no equivalence witness exists without a transport law"],
                "lens_artifacts": {},
            },
        },
    )
    _write_json(
        executions_dir / "index.json",
        {
            "metadata": {"kb_ref": "demo", "execution_count": 1},
            "executions": [
                {
                    "execution_id": "discexec.demo.001",
                    "branch_id": "disclayer.demo.family.equivalence",
                    "artifact_json": str(execution_report_path),
                    "artifact_md": str(executions_dir / "equivalence.md"),
                }
            ],
        },
    )

    report = build_report(artifacts_dir=artifacts_dir, kb_ref="demo", repo_root=repo_root)

    package = report["expert_conjectures"][0]
    assert package["mathematical_layers"]["quantifier_signature"] == native_layers["quantifier_signature"]
    assert package["mathematical_layers"]["lean_style"]["theorem_name"] == "native_transport_packet"
