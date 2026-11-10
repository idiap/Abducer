# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for breakthrough profiling over blocked discovery frontiers."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
PROVE_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-prove-cycle" / "scripts"
PROFILE_SCRIPT_DIR = ROOT / "skills" / "evaluation" / "kb-discovery-breakthrough-profiler" / "scripts"

for path in (COMMON_DIR, PROVE_SCRIPT_DIR, PROFILE_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from generate_discovery_breakthrough_profile import (
    build_discovery_lens_artifacts,
    build_discovery_pattern_routing,
    build_expanded_prompt_pack,
    build_prompt_pack,
    build_report,
)
from generate_discovery_breakthrough_profile import spawn_discovery_branches


def test_breakthrough_profile_classifies_obstruction_families() -> None:
    prior_art = {
        "search_justification": "Queue exhausted.",
        "obstruction_map": [
            {
                "name": "carrier-realization",
                "reference_ids": ["mathlibref.demo.001"],
                "titles": ["Known magnification theorem"],
                "queue_ids": ["proofq.demo.001"],
                "what_changed": ["Target is grounded; bridge is still open."],
            },
            {
                "name": "pit-upgrade",
                "reference_ids": ["mathlibref.demo.002"],
                "titles": ["Known PIT theorem"],
                "queue_ids": ["proofq.demo.002"],
                "what_changed": ["Need explicit generator, not just semantics."],
            },
            {
                "name": "target-alignment",
                "reference_ids": ["mathlibref.demo.003"],
                "titles": ["Known alignment theorem"],
                "queue_ids": ["proofq.demo.003"],
                "what_changed": ["Need correspondence to the target object class."],
            },
        ],
    }
    queue = {
        "entries": [
            {
                "queue_id": "proofq.demo.001",
                "title": "Carrier Realization Lemma",
                "priority": 0.71,
                "conjecture_statement": "Construct an explicit carrier.",
            },
            {
                "queue_id": "proofq.demo.002",
                "title": "PIT Upgrade Lemma",
                "priority": 0.66,
                "conjecture_statement": "Upgrade semantic object to explicit PIT.",
            },
            {
                "queue_id": "proofq.demo.003",
                "title": "Alignment Lemma",
                "priority": 0.62,
                "conjecture_statement": "Identify the target object-class correspondence.",
            },
        ]
    }

    report = build_report(prior_art=prior_art, queue=queue, kb_ref="demo")
    assert report["metadata"]["profile_count"] == 3
    top = report["profiles"][0]
    assert top["obstruction_class"] == "carrier-realization"
    assert top["breakthrough_family"] == "realization"
    assert "explicit mathematical object family" in top["required_move"]

    pit = next(row for row in report["profiles"] if row["obstruction_class"] == "pit-upgrade")
    assert pit["breakthrough_family"] == "explicitness"
    assert pit["major_subresult_type"] == "bridge object/tool"

    prompt_pack = build_prompt_pack(report)
    assert prompt_pack["metadata"]["prompt_family_count"] >= 4
    realization_prompt = next(
        row for row in prompt_pack["prompt_packs"] if row["breakthrough_family"] == "realization"
    )
    assert "explicit mathematical object family" in realization_prompt["system_prompt"]
    explicitness_prompt = next(
        row for row in prompt_pack["prompt_packs"] if row["breakthrough_family"] == "explicitness"
    )
    assert "algorithmic one" in explicitness_prompt["system_prompt"]
    categorical_prompt = next(
        row for row in prompt_pack["prompt_packs"] if row["breakthrough_family"] == "categorical-reframing"
    )
    assert categorical_prompt["epistemic_lens"] == "category-theoretic"
    assert categorical_prompt["routing_heuristic"]["recommended"] is True
    assert categorical_prompt["routing_heuristic"]["score"] >= categorical_prompt["routing_heuristic"]["threshold"]
    assert categorical_prompt["routing_heuristic"]["active_criteria"]
    assert categorical_prompt["lens_artifacts"]["diagram_candidates"]
    assert "non_commuting_route" in categorical_prompt["lens_artifacts"]["negative_outputs"]
    hott_prompt = next(
        row for row in prompt_pack["prompt_packs"] if row["breakthrough_family"] == "equivalence-coherence-reframing"
    )
    assert hott_prompt["epistemic_lens"] == "hott"
    assert hott_prompt["routing_heuristic"]["recommended"] is True
    assert hott_prompt["routing_heuristic"]["score"] >= hott_prompt["routing_heuristic"]["threshold"]
    assert hott_prompt["routing_heuristic"]["active_criteria"]
    assert hott_prompt["lens_artifacts"]["equivalence_claims"]
    assert "transport_incoherent" in hott_prompt["lens_artifacts"]["negative_outputs"]

    expanded = build_expanded_prompt_pack(report)
    assert expanded["metadata"]["epistemic_pattern_count"] >= 1
    invariant_prompt = next(
        row for row in expanded["epistemic_patterns"] if row["pattern_id"] == "invariant-discovery"
    )
    assert "preserve" in invariant_prompt["system_prompt"].lower()

    routing = build_discovery_pattern_routing(report, expanded)
    assert routing["metadata"]["layer_count"] == (
        expanded["metadata"]["prompt_family_count"] + expanded["metadata"]["epistemic_pattern_count"]
    )
    assert routing["metadata"]["family_layer_count"] == expanded["metadata"]["prompt_family_count"]
    assert routing["metadata"]["pattern_layer_count"] == expanded["metadata"]["epistemic_pattern_count"]
    assert routing["recommended_layer_order"][0]["layer_kind"] != routing["recommended_layer_order"][1]["layer_kind"]
    assert routing["dispatch_rounds"][0]["layer_ids"]
    assert any(row["layer_kind"] == "breakthrough-family" for row in routing["discovery_layers"])
    assert any(row["layer_kind"] == "epistemic-pattern" for row in routing["discovery_layers"])
    realization_layer = next(
        row for row in routing["discovery_layers"] if row["target_id"] == "realization"
    )
    gate = realization_layer["external_framework_search"]
    assert gate["recommended"] is True
    assert gate["mode"] == "targeted-foundation-search"
    assert "proof complexity" in gate["candidate_framework_regions"][0].lower()
    categorical_layer = next(
        row for row in routing["discovery_layers"] if row["target_id"] == "categorical-reframing"
    )
    assert categorical_layer["epistemic_lens"] == "category-theoretic"
    assert categorical_layer["routing_heuristic"]["recommended"] is True
    assert categorical_layer["lens_artifacts"]["commutativity_obligations"]
    hott_layer = next(
        row for row in routing["discovery_layers"] if row["target_id"] == "equivalence-coherence-reframing"
    )
    assert hott_layer["epistemic_lens"] == "hott"
    assert hott_layer["routing_heuristic"]["recommended"] is True
    assert hott_layer["lens_artifacts"]["coherence_failures"]

    lens_artifacts = build_discovery_lens_artifacts(report, prompt_pack, routing)
    assert lens_artifacts["metadata"]["lens_count"] == 2
    assert {row["lens_id"] for row in lens_artifacts["lenses"]} == {
        "categorical-reframing",
        "equivalence-coherence-reframing",
    }


def test_breakthrough_profile_spawns_persistent_discovery_branches(tmp_path: Path) -> None:
    report = {
        "metadata": {"kb_ref": "demo"},
        "profiles": [
            {
                "obstruction_class": "carrier-realization",
                "breakthrough_family": "realization",
                "required_move": "Realize an explicit carrier.",
                "abstraction_required": "A witness family with admissibility conditions.",
                "minimal_theorem_shape": "If S then construct C forcing T.",
                "major_subresult_type": "bridge object/tool",
                "search_modes": ["explicit carrier construction"],
                "anti_patterns": ["renaming the carrier"],
                "queue_ids": ["proofq.demo.001"],
                "reference_ids": ["mathlibref.demo.001"],
                "effect_notes": ["Target already grounded."],
                "pressure_score": 1.0,
                "top_priority": 0.9,
                "sample_theorem_targets": ["Construct C."],
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
                "queue_ids": ["proofq.demo.002"],
                "reference_ids": ["mathlibref.demo.002"],
                "effect_notes": ["The route is blocked by missing correspondence."],
                "pressure_score": 0.8,
                "top_priority": 0.7,
                "sample_theorem_targets": ["Construct D from C."],
            },
        ],
    }
    prompt_pack = build_expanded_prompt_pack(report)
    routing = build_discovery_pattern_routing(report, prompt_pack)
    state, branch_paths, dossiers = spawn_discovery_branches(routing, artifacts_dir=tmp_path, activate_top_k=2)
    assert branch_paths[0].exists()
    assert branch_paths[1].exists()
    assert state["metadata"]["branch_count"] == routing["metadata"]["layer_count"]
    assert state["metadata"]["active_count"] >= 1
    assert state["branches"][0]["pdl_program"]["metadata"]["kind"] == "discovery-branch"
    assert any(
        row.get("target_id") == "categorical-reframing" and row.get("lens_artifacts", {}).get("diagram_candidates")
        for row in state["branches"]
    )
    assert any(
        row.get("target_id") == "equivalence-coherence-reframing" and row.get("lens_artifacts", {}).get("equivalence_claims")
        for row in state["branches"]
    )
    assert any(
        row.get("target_id") == "categorical-reframing" and row.get("routing_heuristic", {}).get("recommended") is True
        for row in state["branches"]
    )
    assert any(
        row.get("target_id") == "equivalence-coherence-reframing"
        and row.get("routing_heuristic", {}).get("recommended") is True
        for row in state["branches"]
    )
    assert dossiers
    categorical_dossier = next(
        row for row in dossiers if "categorical-reframing" in row["md"]
    )
    dossier_payload = json.loads(Path(categorical_dossier["json"]).read_text(encoding="utf-8"))
    assert dossier_payload["pdl_program"]["metadata"]["kind"] == "discovery-branch"
    assert Path(categorical_dossier["json"]).exists()
    assert Path(categorical_dossier["md"]).exists()
    dossier_md = Path(categorical_dossier["md"]).read_text(encoding="utf-8")
    assert "Knowledge Source Invocation Policy" in dossier_md
    assert "## PDL Program" in dossier_md
    assert "## Lens Artifacts" in dossier_md
    assert "Routing heuristic: recommended=True" in dossier_md
    assert "Active criteria:" in dossier_md
