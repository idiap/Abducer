# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_search_space_tree import _build_report


def test_search_space_tree_persists_route_history_and_tree_shape(tmp_path: Path) -> None:
    artifacts = tmp_path / "artifacts" / "mini"
    artifacts.mkdir(parents=True, exist_ok=True)
    state_path = tmp_path / "artifacts" / "search-space-state" / "mini.json"

    bridge_plan = {
        "bridge_programs": [
            {
                "bridge_id": "bridge.001",
                "from_id": "st.def.magnify",
                "to_id": "st.thm.sep",
                "bridge_type": "magnification bridge",
                "bridge_score": 0.7,
                "effective_bridge_score": 0.7,
                "inferential_commitment": {
                    "hypothesis_id": "phyp.001",
                    "target_consequence_schema": "NP-not-in-P/poly",
                    "preserved_invariant": "MCSP complexity profile",
                },
                "statement_delta": {
                    "source_problem_family": "MCSP",
                    "target_problem_family": "MCSP",
                    "model_shift": "nonuniform-circuits",
                    "target_claim_focus": "NP not in P/poly",
                    "typed_object_expectation": "hardness-magnification witness family",
                    "route_synopsis": "Move from st.def.magnify to st.thm.sep.",
                },
            }
        ]
    }
    conjectures = {
        "abstraction_conjectures": [
            {
                "conjecture_id": "conj.001",
                "bridge_id": "bridge.001",
                "abstraction_label": "MCSP witness family",
                "abstraction_type": "intermediate-complexity-measure",
                "carrier_kind": "family of instances",
                "typing_status": "typed",
            }
        ]
    }
    proofs = {
        "proof_sketches": [
            {
                "sketch_id": "psk.001",
                "bridge_id": "bridge.001",
                "conjecture_id": "conj.001",
                "title": "MCSP witness route",
                "proof_strategy_family": "invariant-lift-through-intermediate-object",
                "sketch_score": 0.9,
                "hypothesis_ids": ["phyp.001"],
            }
        ]
    }
    hyp_eval = {
        "results": [
            {
                "hypothesis_id": "phyp.001",
                "verdict": "inconclusive",
                "next_status": "needs-testing",
            }
        ]
    }

    (artifacts / "bridge-plan.json").write_text(__import__("json").dumps(bridge_plan), encoding="utf-8")
    (artifacts / "concept-gap-abstractions.json").write_text(__import__("json").dumps(conjectures), encoding="utf-8")
    (artifacts / "proof-sketches.json").write_text(__import__("json").dumps(proofs), encoding="utf-8")
    (artifacts / "hypothesis-evaluation.json").write_text(__import__("json").dumps(hyp_eval), encoding="utf-8")

    initial_state = {
        "metadata": {"kb_ref": "mini", "created_utc": "2026-03-16T00:00:00+00:00"},
        "branches": {},
    }
    report, new_state = _build_report(
        artifacts_dir=artifacts,
        kb_ref="mini",
        run_id="run-1",
        state_path=state_path,
        state=initial_state,
    )

    assert report["metadata"]["route_count"] == 1
    assert report["frontier"]["resume"][0]["bridge_id"] == "bridge.001"
    assert report["tree"]["children"][0]["dimension"] == "problem-family"
    branch = next(iter(new_state["branches"].values()))
    assert branch["visit_count"] == 1
    assert branch["latest_outcome"] == "open"
    assert branch["conjecture_count"] == 1
    assert branch["proof_sketch_count"] == 1
