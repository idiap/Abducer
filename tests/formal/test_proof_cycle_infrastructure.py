# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for discovery/prove cycle infrastructure."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
DISCOVERY_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-discovery-cycle" / "scripts"
PROVE_SCRIPT_DIR = ROOT / "skills" / "discovery" / "kb-prove-cycle" / "scripts"

for path in (COMMON_DIR, DISCOVERY_SCRIPT_DIR, PROVE_SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from discovery_branch_queue import load_discovery_branch_state
from enqueue_proof_candidates import build_queue_entries, build_repair_lemma_entries, build_repair_queue_entries
import finalize_proof_cycle as finalize_proof_cycle_module
from finalize_proof_cycle import _seed_high_reward_followups
from finalize_proof_cycle import _maybe_generate_produced_paper
from finalize_proof_cycle import _normalize_major_subresult_assessment
from finalize_proof_cycle import _persist_external_references
from finalize_proof_cycle import main as finalize_proof_cycle_main
from high_reward_watch import default_high_reward_watch, save_high_reward_watch, load_high_reward_watch
from generate_proof_cycle_summary import build_summary, refresh_summary_from_sources, render_markdown
from negative_route_heuristic import build_negative_route_heuristic
from problem_mathlib import append_mathlib_result, default_mathlib, load_mathlib_index, save_mathlib_index, search_mathlib
from proof_queue import consume_next_entry, default_queue, enqueue_entries, finalize_queue_entry, load_proof_queue, proof_queue_paths, render_proof_queue_markdown, save_proof_queue
from start_proof_cycle import build_attempt_record, render_attempt_markdown


def _bridge() -> dict:
    return {
        "bridge_id": "bridge.001",
        "priority": 0.91,
        "source_statement_id": "st.src",
        "target_statement_id": "st.tgt",
        "source_excerpt": "Source theorem excerpt.",
        "target_excerpt": "Target theorem excerpt.",
        "route_synopsis": "Move from st.src toward st.tgt through a witness family.",
        "abstraction_label": "Witness family",
        "carrier_kind": "family of instances equipped with a witness measure",
        "preserved_invariant": "witness complexity profile",
        "proof_strategy_family": "invariant-lift-through-intermediate-object",
        "missing_route_lemma": "Prove the witness family transfers the lower bound to the target.",
        "conditional_proposition": "If the witness family exists, the target consequence follows.",
        "proof_obligations": ["Build the witness family from the source theorem."],
        "candidate_lemmas": ["The source theorem induces the witness family."],
        "negative_route": "Allow the witness family to ignore source-side content.",
        "failure_diagnosis": "The route fails if the witness family is only topical overlap.",
        "statement_delta": {
            "source_claim_focus": "explicit source lower bound",
            "target_claim_focus": "major target separation",
        },
    }


def test_discovery_cycle_builds_and_enqueues_concrete_proof_targets() -> None:
    expert = {
        "recommended_bridges": [
            _bridge(),
            {
                **_bridge(),
                "bridge_id": "bridge.002",
                "target_statement_id": "st.tgt.2",
                "missing_route_lemma": "Prove the witness family reaches the second target.",
            },
        ]
    }
    search_space = {
        "frontier": {
            "resume": [
                {
                    "bridge_id": "bridge.001",
                    "policy": "resume-with-deeper-proof",
                    "priority": 0.96,
                },
                {
                    "bridge_id": "bridge.002",
                    "policy": "resume-with-deeper-proof",
                    "priority": 0.88,
                }
            ]
        },
        "routes": [
            {
                "bridge_id": "bridge.001",
                "route_signature": "route.demo.001",
                "priority": 0.95,
                "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"},
            },
            {
                "bridge_id": "bridge.002",
                "route_signature": "route.demo.002",
                "priority": 0.87,
                "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt.2"},
            }
        ],
    }

    entries = build_queue_entries(expert=expert, search_space=search_space, kb_ref="demo", top_k=3)
    assert len(entries) == 2
    assert entries[0]["claim_type"] == "route-conjecture"
    assert entries[0]["bridge_id"] == "bridge.001"
    assert entries[0]["exploration_policy"] == "resume-with-deeper-proof"
    assert entries[0]["conjecture_statement"].startswith("There exists an admissible Witness family")
    assert "major target separation" in entries[0]["claim_text"]

    queue = default_queue(kb_ref="demo")
    added, updated = enqueue_entries(queue, entries)
    assert added == 2
    assert updated == 0
    assert queue["entries"][0]["queue_id"] == "proofq.demo.001"
    assert queue["entries"][1]["queue_id"] == "proofq.demo.002"
    assert queue["entries"][0]["claim_text"].startswith("There exists an admissible Witness family")
    assert queue["entries"][0]["pdl_program"]["metadata"]["kind"] == "queue-entry"
    assert queue["entries"][0]["pdl_program"]["bridge_object"]["label"] == "Witness family"
    assert queue["entries"][0]["mathematical_layers"]["latex"]["theorem_statement"].startswith(r"\forall W")
    heuristic = queue["entries"][0]["negative_reasoning_program"]["heuristic"]
    assert heuristic["decision"] == "parallel"
    assert heuristic["use_negation"] is True
    assert heuristic["use_impossibility_claim"] is True


def test_enqueue_entries_defers_non_self_contained_queue_item() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture-placeholder",
                "title": "Carrier C...",
                "priority": 0.94,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "If source theorem S holds in regime R, then carrier C transports the route to target theorem T.",
                "conjecture_statement": "If source theorem S holds in regime R, then carrier C transports the route to target theorem T.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Move from source theorem S toward target theorem T through carrier C...",
                "candidate_object": "unspecified witness family",
                "carrier_kind": "family of instances",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Prove carrier C preserves witness profile while reaching target theorem T.",
            }
        ],
    )
    row = queue["entries"][0]
    contract = row["interpretability_contract"]

    assert row["status"] == "deferred"
    assert row["deferred_by"] == "llm-interpretability-gate"
    assert contract["ready"] is False
    assert any("schema placeholders" in issue for issue in contract["blockers"])
    assert any("truncation markers" in issue for issue in contract["blockers"])
    assert row["inference_diagnosis"]["context_status"] == "ill-posed"
    assert row["inference_diagnosis"]["inference_status"] == "underdetermined"
    assert row["inference_diagnosis"]["certainty_now"] == "very-low"


def test_queue_refresh_reopens_entry_once_it_is_reencoded_as_self_contained() -> None:
    queue = default_queue(kb_ref="demo")
    original = {
        "queue_key": "bridge.001|st.tgt|route-conjecture-placeholder",
        "title": "Carrier C...",
        "priority": 0.94,
        "bridge_id": "bridge.001",
        "claim_type": "route-conjecture",
        "claim_text": "If source theorem S holds in regime R, then carrier C transports the route to target theorem T.",
        "conjecture_statement": "If source theorem S holds in regime R, then carrier C transports the route to target theorem T.",
        "source_statement_id": "st.src",
        "target_statement_id": "st.tgt",
        "source_excerpt": "Source theorem excerpt.",
        "target_excerpt": "Target theorem excerpt.",
        "route_synopsis": "Move from source theorem S toward target theorem T through carrier C...",
        "candidate_object": "unspecified witness family",
        "carrier_kind": "family of instances",
        "preserved_invariant": "witness profile",
        "missing_route_lemma": "Prove carrier C preserves witness profile while reaching target theorem T.",
    }
    enqueue_entries(queue, [original])
    assert queue["entries"][0]["status"] == "deferred"

    refreshed = {
        **original,
        "title": "Witness family transport theorem",
        "claim_text": "There exists an admissible Witness family whose transport law carries the source lower bound to the target theorem.",
        "conjecture_statement": "There exists an admissible Witness family whose transport law carries the source lower bound to the target theorem.",
        "route_synopsis": "Move from st.src to st.tgt by constructing a Witness family that preserves the witness profile.",
        "candidate_object": "Witness family",
        "missing_route_lemma": "Prove the Witness family transport law preserves the witness profile and triggers the target theorem.",
    }
    added, updated = enqueue_entries(queue, [refreshed])
    row = queue["entries"][0]

    assert added == 0
    assert updated == 1
    assert row["status"] == "pending"
    assert row["deferred_by"] == ""
    assert row["interpretability_contract"]["ready"] is True


def test_interpretability_gate_allows_grounded_theorem_text_with_single_symbolic_parameter() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture-grounded",
                "title": "Witness-family transport theorem",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "A hardness magnification theorem has the form: a barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound.",
                "target_excerpt": "In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers imply major consequences such as NP not in P/poly.",
                "route_synopsis": "Move from st.src on problem MCSP in model nonuniform-circuits toward st.tgt while preserving the witness profile.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of hard instances",
                "preserved_invariant": "witness profile",
                "proof_strategy_family": "transport",
                "missing_route_lemma": "Witness-family transport lemma",
                "negative_route": "Assume the witness family fails to preserve the invariant.",
                "proof_obligations": ["Show the witness family preserves the invariant."],
            }
        ],
    )

    row = queue["entries"][0]
    assert row["status"] == "pending"
    assert row["interpretability_contract"]["ready"] is True
    assert row["inference_diagnosis"]["context_status"] == "well-posed"


def test_negative_route_heuristic_prefers_structural_barriers_but_not_vague_failure() -> None:
    barrier = build_negative_route_heuristic(
        candidate_object="MCSP obstruction family",
        source_focus="barely nontrivial MCSP lower bound",
        target_focus="NP not in P/poly",
        invariant="MCSP complexity profile",
        negative_route="Assume the route remains inside the natural proofs barrier.",
        failure_diagnosis="Any attempt collapses back into the known barrier.",
        barrier_scope="natural-proofs",
        missing_route_lemma="transport law from nonuniform circuits to formulas",
        carrier_kind="family of hard instances",
    )
    assert barrier["decision"] == "negative-first"
    assert barrier["use_contradiction"] is True
    assert barrier["use_impossibility_claim"] is True

    vague = build_negative_route_heuristic(
        candidate_object="bridge object",
        source_focus="",
        target_focus="target consequence",
        invariant="",
        negative_route="",
        failure_diagnosis="",
        barrier_scope="",
        missing_route_lemma="",
        carrier_kind="",
    )
    assert vague["decision"] == "constructive-first"
    assert vague["recommended"] is False


def test_discovery_cycle_backfills_from_bridge_portfolio_when_recommendations_are_exhausted() -> None:
    bridge_one = _bridge()
    bridge_two = {
        **_bridge(),
        "bridge_id": "bridge.002",
        "target_statement_id": "st.tgt.2",
        "statement_delta": {
            "source_claim_focus": "explicit source lower bound",
            "target_claim_focus": "second major target separation",
        },
    }
    bridge_three = {
        **_bridge(),
        "bridge_id": "bridge.003",
        "target_statement_id": "st.tgt.3",
        "statement_delta": {
            "source_claim_focus": "explicit source lower bound",
            "target_claim_focus": "third major target separation",
        },
    }
    expert = {
        "recommended_bridges": [bridge_one],
        "bridge_portfolio": [bridge_one, bridge_two, bridge_three],
    }
    search_space = {
        "frontier": {
            "resume": [
                {"bridge_id": "bridge.001", "policy": "resume-with-deeper-proof", "priority": 0.96},
                {"bridge_id": "bridge.002", "policy": "resume-with-deeper-proof", "priority": 0.88},
                {"bridge_id": "bridge.003", "policy": "resume-with-deeper-proof", "priority": 0.81},
            ]
        },
        "routes": [
            {
                "bridge_id": "bridge.001",
                "route_signature": "route.demo.001",
                "priority": 0.96,
                "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt"},
            },
            {
                "bridge_id": "bridge.002",
                "route_signature": "route.demo.002",
                "priority": 0.88,
                "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt.2"},
            },
            {
                "bridge_id": "bridge.003",
                "route_signature": "route.demo.003",
                "priority": 0.81,
                "dimensions": {"source_statement_id": "st.src", "target_statement_id": "st.tgt.3"},
            },
        ],
    }

    entries = build_queue_entries(expert=expert, search_space=search_space, kb_ref="demo", top_k=3)
    assert len(entries) == 3
    assert [entry["bridge_id"] for entry in entries] == ["bridge.001", "bridge.002", "bridge.003"]


def test_queue_refresh_preserves_in_progress_entry_status() -> None:
    queue = default_queue(kb_ref="demo")
    entries = [
        {
            "queue_key": "bridge.001|st.tgt|route-conjecture",
            "title": "Witness family: target one",
            "priority": 0.91,
            "bridge_id": "bridge.001",
            "claim_type": "route-conjecture",
            "claim_text": "First route conjecture.",
            "conjecture_statement": "First route conjecture.",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt",
        },
        {
            "queue_key": "bridge.002|st.tgt.2|route-conjecture",
            "title": "Witness family: target two",
            "priority": 0.87,
            "bridge_id": "bridge.002",
            "claim_type": "route-conjecture",
            "claim_text": "Second route conjecture.",
            "conjecture_statement": "Second route conjecture.",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt.2",
        },
    ]
    enqueue_entries(queue, entries)

    first = consume_next_entry(queue, attempt_id="attempt.demo.001")
    assert first["queue_id"] == "proofq.demo.001"
    assert first["status"] == "in_progress"

    refreshed_entries = [
        {**entries[0], "status": "pending", "priority": 0.95},
        {**entries[1], "status": "pending", "priority": 0.88},
    ]
    added, updated = enqueue_entries(queue, refreshed_entries)
    assert added == 0
    assert updated == 2
    assert queue["entries"][0]["queue_id"] == "proofq.demo.001"
    assert queue["entries"][0]["status"] == "in_progress"

    second = consume_next_entry(queue, attempt_id="attempt.demo.002")
    assert second["queue_id"] == "proofq.demo.002"
    assert second["status"] == "in_progress"


def test_queue_selection_prefers_constructive_witness_route_over_higher_priority_obstruction_route() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture-obstruction",
                "title": "Obstruction family no-go",
                "priority": 0.95,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "No admissible Obstruction family preserves the witness profile strongly enough to force the target theorem.",
                "conjecture_statement": "No admissible Obstruction family preserves the witness profile strongly enough to force the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Probe whether the obstruction family yields only a local no-go.",
                "candidate_object": "Obstruction family",
                "carrier_kind": "family of obstruction instances",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "No obstruction-family realization reaches the target theorem.",
                "proof_strategy_family": "barrier",
            },
            {
                "queue_key": "bridge.002|st.tgt|route-conjecture-transport",
                "title": "Witness family transport theorem",
                "priority": 0.91,
                "bridge_id": "bridge.002",
                "claim_type": "route-conjecture",
                "claim_text": "For every admissible Witness family, there is a transport law carrying the source lower bound to the target theorem.",
                "conjecture_statement": "For every admissible Witness family, there is a transport law carrying the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Move from st.src to st.tgt through a Witness family transport law.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness profile",
                "missing_route_lemma": "Transport lemma for Witness family",
                "proof_strategy_family": "transport",
            },
        ],
    )

    markdown = render_proof_queue_markdown(queue)
    assert markdown.index("| 1 | proofq.demo.002 | pending |") < markdown.index("| 2 | proofq.demo.001 | pending |")

    selected = consume_next_entry(queue, attempt_id="attempt.demo.001")
    assert selected["queue_id"] == "proofq.demo.002"
    assert selected["status"] == "in_progress"


def test_queue_selection_prefers_higher_governor_value_route_over_higher_raw_priority_side_route() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.013|st.pit|route-conjecture-pit-transport",
                "title": "PIT witness-family transport theorem",
                "priority": 2.107,
                "bridge_id": "bridge.013",
                "claim_type": "route-conjecture",
                "claim_text": "For every admissible PIT witness family, there is a transport law carrying the semantic object to the derandomization target theorem.",
                "conjecture_statement": "For every admissible PIT witness family, there is a transport law carrying the semantic object to the derandomization target theorem.",
                "source_statement_id": "st.pit.src",
                "target_statement_id": "st.pit.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Upgrade a PIT semantic object into a derandomization premise via a witness-family transport law.",
                "candidate_object": "PIT witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "PIT semantic object",
                "missing_route_lemma": "Transport theorem for PIT witness family",
                "proof_strategy_family": "constructive-realization",
                "governor_decision": "major_subresult_candidate",
                "governor_major_subresult_candidate": True,
                "governor_major_subresult_score": 14,
                "governor_value_score": 0.835,
            },
            {
                "queue_key": "bridge.001|st.mcsp|route-conjecture-mcsp-transport",
                "title": "MCSP witness-family transport theorem",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "For every admissible MCSP witness family, there is a transport law carrying the source lower bound to the target theorem.",
                "conjecture_statement": "For every admissible MCSP witness family, there is a transport law carrying the source lower bound to the target theorem.",
                "source_statement_id": "st.mcsp.src",
                "target_statement_id": "st.mcsp.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "route_synopsis": "Carry the magnification route through an MCSP witness-family transport law.",
                "candidate_object": "MCSP witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "MCSP complexity profile in nonuniform-circuits",
                "missing_route_lemma": "Transport theorem for MCSP witness family",
                "proof_strategy_family": "constructive-realization",
                "governor_decision": "major_subresult_candidate",
                "governor_major_subresult_candidate": True,
                "governor_major_subresult_score": 16,
                "governor_value_score": 0.89,
            },
        ],
    )

    markdown = render_proof_queue_markdown(queue)
    assert markdown.index("| 1 | proofq.demo.002 | pending |") < markdown.index("| 2 | proofq.demo.001 | pending |")

    selected = consume_next_entry(queue, attempt_id="attempt.demo.001")
    assert selected["queue_id"] == "proofq.demo.002"
    assert selected["status"] == "in_progress"


def test_build_attempt_record_uses_expert_conjecture_package_context() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture-conjpkg.demo.010",
                "title": "Transport theorem for witness family",
                "priority": 0.95,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "Every admissible Witness family transports the source lower bound to the target regime.",
                "conjecture_statement": "Every admissible Witness family transports the source lower bound to the target regime.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "bridge_object_definition": "A typed family of witness instances mediating the source and target regimes.",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Transport lemma for Witness family",
                "first_nontrivial_lemma_title": "Transport lemma for Witness family",
                "first_nontrivial_lemma_statement": "For every admissible Witness family, the witness complexity profile transports to the target regime.",
                "admissibility_conditions": [
                    "The witness family is explicitly defined on the route.",
                    "The witness family preserves the witness complexity profile.",
                ],
                "negative_barrier_version": "No such transport exists without extra structure.",
                "independent_value_claim": "The transport theorem matters even if the main conjecture remains open.",
                "restricted_regime_mode": "transport-lemma",
                "regime_and_quantifiers": {
                    "quantifier_frame": "For every admissible Witness family in the transport regime.",
                },
                "foundation_search": {
                    "recommended": True,
                    "mode": "targeted-foundation-search",
                    "candidate_framework_regions": ["transport framework"],
                },
                "theorem_package_id": "conjpkg.demo.010",
            }
        ],
    )
    queue_entry = queue["entries"][0]

    attempt = build_attempt_record(
        attempt_id="attempt.demo.010",
        kb_ref="demo",
        queue_entry=queue_entry,
        mathlib_hits=[],
        statement_index={
            "st.src": {"informal": "Source theorem excerpt."},
            "st.tgt": {"informal": "Target theorem excerpt."},
        },
    )

    expert_context = attempt["proof_attempt"]["expert_conjecture_context"]
    assert expert_context["theorem_package_id"] == "conjpkg.demo.010"
    assert expert_context["bridge_object_definition"] == "A typed family of witness instances mediating the source and target regimes."
    assert expert_context["mathematical_layers"]["quantifier_signature"].startswith("For every admissible")
    assert attempt["proof_attempt"]["assumptions"][0] == "For every admissible Witness family in the transport regime."
    assert "The witness family preserves the witness complexity profile." in attempt["proof_attempt"]["assumptions"]
    assert attempt["proof_attempt"]["stepwise_argument"][0]["claim"] == "A typed family of witness instances mediating the source and target regimes."
    assert attempt["proof_attempt"]["stepwise_argument"][1]["claim"] == "For every admissible Witness family, the witness complexity profile transports to the target regime."
    assert attempt["knowledge_source_policy"]["sources"][2]["foundation_search_recommended"] is True
    assert attempt["inference_diagnosis"]["context_status"] == "well-posed"
    assert attempt["inference_diagnosis"]["inference_status"] == "difficult-but-well-posed"

    markdown = render_attempt_markdown(attempt)
    assert "## Prompt / Inference Diagnosis" in markdown
    assert "- Context status: well-posed" in markdown
    assert "## Expert Theorem Package" in markdown
    assert "## Mathematical Packet" in markdown
    assert "- Theorem package ID: conjpkg.demo.010" in markdown
    assert "- Negative/barrier version: No such transport exists without extra structure." in markdown
    assert "```lean" in markdown


def test_queue_allows_second_order_claims_for_same_bridge_target() -> None:
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
                "conjecture_statement": "Primary route conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
            }
        ],
    )
    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="blocked",
        result_id="",
        attempt_id="attempt.demo.001",
        summary="Primary route blocked.",
    )

    added, updated = enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|abstraction-conjecture-conj-002",
                "title": "Repair conjecture",
                "priority": 0.83,
                "bridge_id": "bridge.001",
                "claim_type": "abstraction-conjecture",
                "conjecture_id": "conj.002",
                "claim_text": "Repair conjecture.",
                "conjecture_statement": "Repair conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Obstruction family",
            }
        ],
    )

    assert added == 1
    assert updated == 0
    assert len(queue["entries"]) == 2
    assert {row["claim_type"] for row in queue["entries"]} == {"route-conjecture", "abstraction-conjecture"}


def test_discovery_cycle_builds_repair_entries_from_blocked_routes() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Witness family: major target separation",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "Primary route conjecture.",
                "conjecture_statement": "Primary route conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
            }
        ],
    )
    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="blocked",
        result_id="",
        attempt_id="attempt.demo.001",
        summary="Carrier equivalence theorem is missing.",
    )

    gap_abstractions = {
        "conjectures": [
            {
                "conjecture_id": "conj.002",
                "bridge_id": "bridge.001",
                "from_id": "st.src",
                "to_id": "st.tgt",
                "abstraction_type": "canonical-obstruction-family",
                "abstraction_label": "Witness obstruction family",
                "carrier_kind": "family of hard instances",
                "typing_status": "typed",
                "preserved_invariant": "witness complexity profile",
                "priority": 0.77,
                "statement_delta": {
                    "source_claim_focus": "explicit source lower bound",
                    "target_claim_focus": "major target separation",
                    "source_theorem_excerpt": "Source theorem excerpt.",
                    "target_theorem_excerpt": "Target theorem excerpt.",
                    "route_synopsis": "Repair the blocked route by promoting a stronger carrier.",
                },
                "definitional_profile": {
                    "bridging_concept_definition": "An adequate obstruction-family bridge concept is a family of hard instances that forces the target payoff."
                },
                "mathematical_specification": {
                    "missing_route_lemma": "Show the stronger carrier yields the target separation.",
                    "conditional_claim": "If the stronger carrier exists, the target separation follows.",
                    "proof_obligation_templates": [
                        "Build the stronger carrier from the source lower bound.",
                        "Show the stronger carrier forces the target separation.",
                    ],
                    "inspection_focus": [
                        "Specify the carrier.",
                        "State the first forcing lemma.",
                    ],
                    "obstruction_template": "The repair fails if the stronger carrier is only topical overlap.",
                },
                "counterfactual_probes": [
                    {
                        "intervention": "Discard the stronger carrier and keep only shared vocabulary.",
                    }
                ],
            }
        ]
    }

    entries = build_repair_queue_entries(gap_abstractions=gap_abstractions, queue=queue, kb_ref="demo", top_k=3)
    assert len(entries) == 1
    assert entries[0]["claim_type"] == "abstraction-conjecture"
    assert entries[0]["bridge_id"] == "bridge.001"
    assert entries[0]["candidate_object"] == "Witness obstruction family"
    assert "family of hard instances" in entries[0]["conjecture_statement"]
    assert entries[0]["exploration_policy"] == "re-encode-blocked-route"


def test_discovery_cycle_prioritizes_repairs_by_breakthrough_family() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt.a|route-conjecture",
                "title": "MCSP route A",
                "priority": 0.94,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "Route A.",
                "conjecture_statement": "Route A.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.a",
                "candidate_object": "Witness family A",
            },
            {
                "queue_key": "bridge.002|st.tgt.b|route-conjecture",
                "title": "MCSP route B",
                "priority": 0.91,
                "bridge_id": "bridge.002",
                "claim_type": "route-conjecture",
                "claim_text": "Route B.",
                "conjecture_statement": "Route B.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.b",
                "candidate_object": "Witness family B",
            },
            {
                "queue_key": "bridge.003|st.tgt.c|route-conjecture",
                "title": "Alignment route",
                "priority": 0.62,
                "bridge_id": "bridge.003",
                "claim_type": "route-conjecture",
                "claim_text": "Route C.",
                "conjecture_statement": "Route C.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt.c",
                "candidate_object": "Witness family C",
            },
        ],
    )
    finalize_queue_entry(queue, queue_id="proofq.demo.001", outcome="blocked", result_id="", attempt_id="attempt.demo.001", summary="Blocked.")
    finalize_queue_entry(queue, queue_id="proofq.demo.002", outcome="blocked", result_id="", attempt_id="attempt.demo.002", summary="Blocked.")
    finalize_queue_entry(queue, queue_id="proofq.demo.003", outcome="blocked", result_id="", attempt_id="attempt.demo.003", summary="Blocked.")

    gap_abstractions = {
        "conjectures": [
            {
                "conjecture_id": "conj.001",
                "bridge_id": "bridge.001",
                "from_id": "st.src",
                "to_id": "st.tgt.a",
                "abstraction_type": "canonical-obstruction-family",
                "abstraction_label": "Witness obstruction family A",
                "carrier_kind": "family of hard instances",
                "typing_status": "typed",
                "preserved_invariant": "witness complexity profile",
                "priority": 0.84,
                "statement_delta": {
                    "source_claim_focus": "source lower bound A",
                    "target_claim_focus": "target separation A",
                },
                "definitional_profile": {"bridging_concept_definition": "Carrier A."},
                "mathematical_specification": {"conditional_claim": "Carrier A forces the target."},
            },
            {
                "conjecture_id": "conj.002",
                "bridge_id": "bridge.002",
                "from_id": "st.src",
                "to_id": "st.tgt.b",
                "abstraction_type": "canonical-obstruction-family",
                "abstraction_label": "Witness obstruction family B",
                "carrier_kind": "family of hard instances",
                "typing_status": "typed",
                "preserved_invariant": "witness complexity profile",
                "priority": 0.81,
                "statement_delta": {
                    "source_claim_focus": "source lower bound B",
                    "target_claim_focus": "target separation B",
                },
                "definitional_profile": {"bridging_concept_definition": "Carrier B."},
                "mathematical_specification": {"conditional_claim": "Carrier B forces the target."},
            },
            {
                "conjecture_id": "conj.003",
                "bridge_id": "bridge.003",
                "from_id": "st.src",
                "to_id": "st.tgt.c",
                "abstraction_type": "surrogate-promise-problem",
                "abstraction_label": "Alignment carrier",
                "carrier_kind": "promise problem family",
                "typing_status": "typed",
                "preserved_invariant": "alignment invariant",
                "priority": 0.63,
                "statement_delta": {
                    "source_claim_focus": "source lower bound C",
                    "target_claim_focus": "target separation C",
                },
                "definitional_profile": {"bridging_concept_definition": "Carrier C."},
                "mathematical_specification": {"conditional_claim": "Carrier C forces the target."},
            },
        ]
    }
    breakthrough_profile = {
        "profiles": [
            {
                "obstruction_class": "carrier-realization",
                "breakthrough_family": "realization",
                "pressure_score": 5.0,
                "top_priority": 0.94,
                "queue_ids": ["proofq.demo.001", "proofq.demo.002"],
            },
            {
                "obstruction_class": "target-alignment",
                "breakthrough_family": "alignment",
                "pressure_score": 1.5,
                "top_priority": 0.62,
                "queue_ids": ["proofq.demo.003"],
            },
        ]
    }

    entries = build_repair_queue_entries(
        gap_abstractions=gap_abstractions,
        queue=queue,
        kb_ref="demo",
        breakthrough_profile=breakthrough_profile,
        top_k=2,
    )
    assert len(entries) == 2
    assert entries[0]["breakthrough_family"] == "realization"
    assert entries[1]["breakthrough_family"] == "alignment"
    assert entries[1]["bridge_id"] == "bridge.003"


def test_discovery_cycle_builds_repair_lemma_entries_from_blocked_abstractions(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.002|st.tgt|abstraction-conjecture-conj-005",
                "title": "MCSP obstruction family: target",
                "priority": 0.71,
                "bridge_id": "bridge.002",
                "claim_type": "abstraction-conjecture",
                "conjecture_id": "conj.005",
                "claim_text": "Abstraction conjecture.",
                "conjecture_statement": "Abstraction conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "MCSP obstruction family",
                "carrier_kind": "family of hard instances",
                "preserved_invariant": "witness complexity profile",
                "route_synopsis": "Move from st.src to st.tgt through a formula-size route.",
                "missing_route_lemma": "Prove the formula-size transport theorem.",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt mentioning formula-size.",
            }
        ],
    )
    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="blocked",
        result_id="",
        attempt_id="attempt.demo.010",
        summary="The stronger carrier requirement clarifies the object sought, but the current artifacts still lack both a realized hard family and the nonuniform-circuits -> formula-size transport theorem.",
    )

    attempt_payload = {
        "metadata": {"attempt_id": "attempt.demo.010"},
        "target": {
            "bridge_id": "bridge.002",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt",
            "candidate_object": "MCSP obstruction family",
            "carrier_kind": "family of hard instances",
            "preserved_invariant": "witness complexity profile",
            "route_synopsis": "Move from st.src to st.tgt through a formula-size route.",
            "missing_route_lemma": "Prove the formula-size transport theorem.",
            "source_excerpt": "Source theorem excerpt.",
            "target_excerpt": "Target theorem excerpt mentioning formula-size.",
            "statement_delta": {
                "source_claim_focus": "source lower bound",
                "target_claim_focus": "formula-size consequence",
            },
        },
        "proof_attempt": {
            "result_statement": "No local transport theorem reaches the formula-size regime.",
        },
        "final_assessment": {
            "summary": "The stronger carrier requirement clarifies the object sought, but the current artifacts still lack both a realized hard family and the nonuniform-circuits -> formula-size transport theorem."
        },
    }
    (attempts_dir / "attempt.demo.010.json").write_text(
        __import__("json").dumps(attempt_payload, indent=2) + "\n",
        encoding="utf-8",
    )

    entries = build_repair_lemma_entries(artifacts_dir=artifacts_dir, queue=queue, kb_ref="demo", top_k=4)
    assert len(entries) == 1
    assert entries[0]["claim_type"] == "repair-lemma"
    assert "Formula-Size Transport Lemma" in entries[0]["title"]
    assert "formula-size regime" in entries[0]["conjecture_statement"]
    assert entries[0]["exploration_policy"] == "repair-blocked-abstraction"


def test_prove_cycle_attempt_mathlib_and_summary_roundtrip() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|prove-the-witness-family",
                "title": "Witness family: major target separation",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "There exists an admissible Witness family such that an explicit source lower bound can be transported to a major target separation.",
                "conjecture_statement": "There exists an admissible Witness family such that an explicit source lower bound can be transported to a major target separation.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness complexity profile",
                "proof_strategy_family": "invariant-lift-through-intermediate-object",
                "missing_route_lemma": "Prove the witness family transfers the lower bound to the target.",
                "proof_obligations": ["Build the witness family."],
                "negative_route": "Assume the witness family fails to preserve the witness complexity profile.",
                "negative_reasoning_program": {
                    "negative_mode": "non-realization",
                    "negated_claim": "Assume the witness family cannot be realized as a mathematically usable carrier.",
                    "contradiction_target": "Localize failure to carrier realization or invariant preservation.",
                    "forbidden_outcome": "The witness family is only topical overlap.",
                    "impossibility_claim_template": "No admissible carrier realizing the witness family currently preserves the witness complexity profile strongly enough to force the target separation.",
                },
                "impossibility_conjecture": "No admissible carrier realizing the witness family currently preserves the witness complexity profile strongly enough to force the target separation.",
            }
        ],
    )
    queue_entry = queue["entries"][0]

    mathlib = default_mathlib(kb_ref="demo")
    append_mathlib_result(
        mathlib,
        {
            "result_id": "mathlib.demo.001",
            "title": "Witness family auxiliary lemma",
            "statement": "A local auxiliary witness lemma.",
            "summary": "Useful local support result.",
            "outcome": "proved",
            "artifact_path": "InformalMathLib/demo/positive-results/mathlib.demo.001-witness-family-auxiliary-lemma.md",
            "updated_utc": "2026-03-16T00:00:00+00:00",
            "tags": ["Witness family", "st.tgt"],
        },
    )
    hits = search_mathlib(mathlib, ["Witness family", "st.tgt"], limit=3)
    assert len(hits) == 1

    attempt = build_attempt_record(
        attempt_id="attempt.demo.001",
        kb_ref="demo",
        queue_entry=queue_entry,
        mathlib_hits=hits,
        statement_index={
            "st.src": {"informal": "Source theorem excerpt."},
            "st.tgt": {"informal": "Target theorem excerpt."},
        },
    )
    assert attempt["metadata"]["queue_id"] == "proofq.demo.001"
    judge_ids = {row["judge_id"] for row in attempt["critique_judges"]}
    assert len(attempt["critique_judges"]) == 13
    assert {
        "statement-grounding",
        "tactic-goal-control",
        "inferential-validity",
        "assumption-discipline",
        "citation-fidelity",
        "proof-granularity",
        "tactic-trace-discipline",
        "tactic-subgoal-exposure",
        "prior-art-and-novelty",
        "local-counterexample-search",
        "obstruction-and-negative-route",
        "contradiction-and-impossibility-discipline",
        "closure",
    } <= judge_ids
    assert attempt["local_context"]["mathlib_hits"][0]["result_id"] == "mathlib.demo.001"
    assert attempt["knowledge_source_policy"]["sources"][0]["source"] == "InformalMathLib"
    assert attempt["external_references"] == []
    assert attempt["proof_attempt"]["theorem_statement"].startswith("There exists an admissible Witness family")
    assert attempt["proof_attempt"]["route_lemma_under_test"] == "Prove the witness family transfers the lower bound to the target."
    assert attempt["proof_attempt"]["informal_tactic_playbook"][0]["tactic_id"] == "normalize-goal"
    assert any(row["tactic_id"] == "negate-goal" for row in attempt["proof_attempt"]["informal_tactic_trace"])
    assert any(row["tactic_id"] == "prove-impossibility-claim" for row in attempt["proof_attempt"]["informal_tactic_trace"])
    assert attempt["proof_attempt"]["contradiction_frame"]["negative_mode"] == "non-realization"
    assert attempt["proof_attempt"]["negative_route_heuristic"]["decision"] == "parallel"
    assert "No admissible carrier realizing the witness family" in attempt["proof_attempt"]["negative_argument"]["impossibility_claim"]
    assert attempt["pdl_program"]["metadata"]["kind"] == "proof-attempt"
    assert attempt["pdl_program"]["bridge_object"]["label"] == "Witness family"
    assert len(attempt["proof_attempt"]["stepwise_argument"]) == 3
    assert all(row["claim"] for row in attempt["proof_attempt"]["stepwise_argument"])
    assert all(row["justification"] for row in attempt["proof_attempt"]["stepwise_argument"])
    assert any(row["tactic_id"] == "reduce-to-route-lemma" for row in attempt["proof_attempt"]["informal_tactic_trace"])
    assert [row["order"] for row in attempt["proof_attempt"]["informal_tactic_trace"]] == list(
        range(1, len(attempt["proof_attempt"]["informal_tactic_trace"]) + 1)
    )
    assert attempt["major_subresult_assessment"]["axes"]["frontier_shift"] == 0
    assert attempt["major_subresult_assessment"]["mandatory_gates"]["self_contained_statement"] is False

    markdown = render_attempt_markdown(attempt)
    assert "## Web Search Gate" in markdown
    assert "## Knowledge Source Invocation Policy" in markdown
    assert "## PDL Program" in markdown
    assert "## External References To Import Into InformalMathLib" in markdown
    assert "### Informal Tactic Playbook" in markdown
    assert "### Informal Tactic Trace" in markdown
    assert "### Negative-Route Heuristic" in markdown
    assert "### Contradiction / Impossibility Frame" in markdown
    assert "## Critique Judges" in markdown
    assert "### Tactic Goal-Control Judge" in markdown
    assert "### Tactic Trace-Discipline Judge" in markdown
    assert "## Major Subresult Assessment" in markdown
    assert "- Conjecture: There exists an admissible Witness family" in markdown
    assert "- Route lemma under test: Prove the witness family transfers the lower bound to the target." in markdown
    assert "- Impossibility claim: No admissible carrier realizing the witness family currently preserves the witness complexity profile strongly enough to force the target separation." in markdown

    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="proved",
        result_id="mathlib.demo.002",
        attempt_id="attempt.demo.001",
        summary="Provisional informal proof recorded.",
    )
    append_mathlib_result(
        mathlib,
        {
            "result_id": "mathlib.demo.002",
            "title": "Witness family main route lemma",
            "statement": "The witness family transfers the lower bound to the target.",
            "summary": "Provisional informal proof recorded.",
            "outcome": "proved",
            "artifact_path": "InformalMathLib/demo/positive-results/mathlib.demo.002-witness-family-main-route-lemma.md",
            "updated_utc": "2026-03-16T00:00:01+00:00",
            "tags": ["Witness family", "route lemma"],
        },
    )

    report = build_summary(kb_ref="demo", queue=queue, mathlib=mathlib)
    assert report["metadata"]["proved_count"] == 2
    assert report["metadata"]["pending_count"] == 0

    summary_markdown = render_markdown(report)
    assert "## Proved" in summary_markdown
    assert "Witness family main route lemma" in summary_markdown


def test_proof_cycle_summary_counts_blocked_queue_entries() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|blocked-route",
                "title": "Witness family blocked route",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "Blocked conjecture.",
                "conjecture_statement": "Blocked conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "missing_route_lemma": "Carrier equivalence theorem is missing.",
            }
        ],
    )
    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="blocked",
        result_id="",
        attempt_id="attempt.demo.003",
        summary="Carrier equivalence theorem is missing.",
    )

    report = build_summary(kb_ref="demo", queue=queue, mathlib=default_mathlib(kb_ref="demo"))
    assert report["metadata"]["blocked_count"] == 1
    assert report["blocked"][0]["queue_id"] == "proofq.demo.001"
    total_underdetermined = (
        report["diagnosis_overview"]["queue"]["inference_counts"]["underdetermined"]
        + report["diagnosis_overview"]["queue_historical"]["inference_counts"]["underdetermined"]
    )
    assert total_underdetermined == 1

    summary_markdown = render_markdown(report)
    assert "## Context Vs Inference Diagnosis" in summary_markdown
    assert "## Blocked Results" in summary_markdown
    assert "Carrier equivalence theorem is missing." in summary_markdown


def test_proof_cycle_summary_deduplicates_blocked_queue_entries_backfilled_into_mathlib() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|blocked-route",
                "title": "Witness family blocked route",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "Blocked conjecture.",
                "conjecture_statement": "Blocked conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
            }
        ],
    )
    finalize_queue_entry(
        queue,
        queue_id="proofq.demo.001",
        outcome="blocked",
        result_id="mathlib.demo.blocked.001",
        attempt_id="attempt.demo.003",
        summary="Carrier equivalence theorem is missing.",
    )

    mathlib = default_mathlib(kb_ref="demo")
    append_mathlib_result(
        mathlib,
        {
            "result_id": "mathlib.demo.blocked.001",
            "queue_id": "proofq.demo.001",
            "attempt_id": "attempt.demo.003",
            "title": "Witness family blocked route",
            "statement": "Blocked conjecture.",
            "summary": "Carrier equivalence theorem is missing.",
            "outcome": "blocked",
            "entry_kind": "negative-local-theorem",
            "artifact_path": "InformalMathLib/demo/negative-results/mathlib.demo.blocked.001.md",
        },
    )

    report = build_summary(kb_ref="demo", queue=queue, mathlib=mathlib)
    assert report["metadata"]["blocked_count"] == 1
    assert report["blocked"][0]["queue_id"] == "proofq.demo.001"


def test_proof_cycle_summary_splits_current_and_historical_diagnosis() -> None:
    queue = default_queue(kb_ref="demo")
    queue["entries"] = [
        {
            "queue_id": "proofq.demo.001",
            "status": "blocked",
            "title": "Current blocked route",
            "claim_text": "Current blocked route.",
            "conjecture_statement": "Current blocked route.",
            "inference_diagnosis": {
                "context_status": "well-posed",
                "inference_status": "difficult-but-well-posed",
                "blocking_defects": [],
            },
        },
        {
            "queue_id": "proofq.demo.002",
            "status": "blocked",
            "title": "Legacy blocked route...",
            "claim_text": "Legacy blocked route...",
            "conjecture_statement": "Legacy blocked route...",
            "inference_diagnosis": {
                "context_status": "ill-posed",
                "inference_status": "underdetermined",
                "blocking_defects": [
                    "`route_synopsis` contains truncation markers, so the theorem state is not self-contained."
                ],
            },
        },
        {
            "queue_id": "proofq.demo.003",
            "status": "deferred",
            "deferred_by": "inactive-discovery-frontier",
            "retired_from_active_frontier": True,
            "title": "Retired branch programme",
            "claim_text": "Retired branch programme.",
            "conjecture_statement": "Retired branch programme.",
            "inference_diagnosis": {
                "context_status": "ill-posed",
                "inference_status": "underdetermined",
                "blocking_defects": [
                    "`claim_text` still uses schema placeholders instead of concrete mathematical content."
                ],
            },
        },
    ]
    attempts = [
        {
            "metadata": {
                "attempt_id": "attempt.demo.001",
                "queue_id": "proofq.demo.001",
                "updated_utc": "2026-03-17T05:00:00+00:00",
                "status": "blocked",
            },
            "status": "blocked",
            "target": {"title": "Current blocked route"},
            "final_assessment": {"outcome": "blocked", "summary": "Older retry."},
            "proof_attempt": {"result_statement": "Older retry."},
            "inference_diagnosis": {
                "context_status": "well-posed",
                "inference_status": "determined",
                "blocking_defects": [],
            },
        },
        {
            "metadata": {
                "attempt_id": "attempt.demo.002",
                "queue_id": "proofq.demo.001",
                "updated_utc": "2026-03-17T06:00:00+00:00",
                "status": "blocked",
            },
            "status": "blocked",
            "target": {"title": "Current blocked route"},
            "final_assessment": {"outcome": "blocked", "summary": "Latest retry."},
            "proof_attempt": {"result_statement": "Latest retry."},
            "inference_diagnosis": {
                "context_status": "well-posed",
                "inference_status": "determined",
                "blocking_defects": [],
            },
        },
        {
            "metadata": {
                "attempt_id": "attempt.demo.003",
                "queue_id": "proofq.demo.002",
                "updated_utc": "2026-03-17T07:00:00+00:00",
                "status": "blocked",
            },
            "status": "blocked",
            "target": {"title": "Legacy blocked route..."},
            "final_assessment": {"outcome": "blocked", "summary": "Legacy packet."},
            "proof_attempt": {"result_statement": "Legacy packet."},
            "inference_diagnosis": {
                "context_status": "ill-posed",
                "inference_status": "underdetermined",
                "blocking_defects": [
                    "`route_synopsis` contains truncation markers, so the theorem state is not self-contained."
                ],
            },
        },
    ]
    report = build_summary(
        kb_ref="demo",
        queue=queue,
        mathlib=default_mathlib(kb_ref="demo"),
        attempts=attempts,
    )

    assert report["metadata"]["queue_current_count"] == 1
    assert report["metadata"]["queue_historical_count"] == 2
    assert report["metadata"]["attempt_current_count"] == 1
    assert report["metadata"]["attempt_historical_count"] == 2
    assert report["diagnosis_overview"]["queue"]["count"] == 1
    assert report["diagnosis_overview"]["queue_historical"]["count"] == 2
    assert report["diagnosis_overview"]["attempts"]["count"] == 1
    assert report["diagnosis_overview"]["attempts_historical"]["count"] == 2

    summary_markdown = render_markdown(report)
    assert "### Queue Historical Archive" in summary_markdown
    assert "### Attempts Historical Archive" in summary_markdown


def test_render_attempt_markdown_uses_current_terminal_state() -> None:
    attempt = build_attempt_record(
        attempt_id="attempt.demo.099",
        kb_ref="demo",
        queue_entry={
            "queue_id": "proofq.demo.099",
            "conjecture_statement": "Demo route conjecture.",
            "bridge_id": "bridge.099",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt",
            "candidate_object": "Witness family",
            "preserved_invariant": "witness invariant",
            "missing_route_lemma": "Route lemma.",
            "proof_strategy_family": "invariant-lift-through-intermediate-object",
        },
        mathlib_hits=[],
        statement_index={},
    )
    attempt["metadata"]["status"] = "blocked"
    attempt["proof_attempt"]["stepwise_argument"] = [
        {
            "step": 1,
            "claim": "The route is blocked.",
            "justification": "A carrier equivalence theorem is missing.",
            "depends_on": ["psk.001", "psk.005"],
        }
    ]
    attempt["proof_attempt"]["negative_argument"] = {
        "obstruction_candidate": "Carrier split.",
        "counterexample_or_barrier": "The two operationalizations are not proved equivalent.",
        "effect_on_claim": "The route remains blocked.",
    }
    attempt["proof_attempt"]["result_statement"] = "Blocked result."
    attempt["proof_attempt"]["result_summary"] = "The route is blocked pending a carrier theorem."
    attempt["critique_judges"][0]["verdict"] = "pass"
    attempt["critique_judges"][0]["notes"] = ["The claim is grounded."]
    attempt["critique_judges"][1]["verdict"] = "fail"
    attempt["critique_judges"][1]["blocking_issues"] = ["No single carrier realizes the route."]
    attempt["final_assessment"] = {
        "outcome": "blocked",
        "verdict": "blocked",
        "novelty_assessment": "No novelty claim.",
        "confidence": "high",
        "summary": "The route is blocked pending a carrier theorem.",
    }
    attempt["major_subresult_assessment"]["overall_judgment"] = "Useful obstruction diagnosis."

    markdown = render_attempt_markdown(attempt)
    assert "## Prompt / Inference Diagnosis" in markdown
    assert "- Inference status: determined" in markdown
    assert "- Status: blocked" in markdown
    assert "normalize-goal" in markdown
    assert "Verdict: pass" in markdown
    assert "Verdict: fail" in markdown
    assert "Notes:" in markdown
    assert "Blocking issues:" in markdown
    assert "- Outcome: blocked" in markdown
    assert "- Result statement: Blocked result." in markdown
    assert "- Overall judgment: Useful obstruction diagnosis." in markdown


def test_proof_cycle_summary_aggregates_attempt_and_queue_diagnoses() -> None:
    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Witness family transport theorem",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "There exists an admissible Witness family that transports the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family that transports the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Transport lemma for Witness family",
                "route_synopsis": "Move from st.src to st.tgt via a Witness family transport law.",
                "proof_strategy_family": "invariant-lift-through-intermediate-object",
                "proof_obligations": ["Build the witness family from the source theorem."],
            }
        ],
    )
    attempt = build_attempt_record(
        attempt_id="attempt.demo.020",
        kb_ref="demo",
        queue_entry=queue["entries"][0],
        mathlib_hits=[],
        statement_index={
            "st.src": {"informal": "Source theorem excerpt."},
            "st.tgt": {"informal": "Target theorem excerpt."},
        },
    )
    report = build_summary(
        kb_ref="demo",
        queue=queue,
        mathlib=default_mathlib(kb_ref="demo"),
        attempts=[attempt],
    )
    assert report["diagnosis_overview"]["queue"]["inference_counts"]["difficult-but-well-posed"] == 1
    assert report["diagnosis_overview"]["attempts"]["inference_counts"]["difficult-but-well-posed"] == 1
    summary_markdown = render_markdown(report)
    assert "### Queue" in summary_markdown
    assert "### Attempts" in summary_markdown


def test_refresh_summary_from_sources_syncs_attempt_status_and_target_from_queue(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    attempts_dir = artifacts_dir / "proof-attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|expert-conjecture",
                "title": "Witness family transport theorem",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "expert-conjecture",
                "claim_text": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "source_excerpt": "Source theorem excerpt.",
                "target_excerpt": "Target theorem excerpt.",
                "candidate_object": "Witness family",
                "carrier_kind": "family of witness instances",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Witness-family transport lemma",
                "route_synopsis": "Move from st.src to st.tgt by constructing a Witness family that preserves the witness profile.",
                "resolution_summary": "The route is now blocked by a local obstruction theorem.",
                "status": "blocked",
            }
        ],
    )
    queue_json, queue_md = proof_queue_paths(repo_root, "demo")
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
    save_mathlib_index(
        default_mathlib(kb_ref="demo"),
        json_path=repo_root / "InformalMathLib" / "demo" / "index.json",
        md_path=repo_root / "InformalMathLib" / "demo" / "catalog.md",
    )

    attempt = {
        "metadata": {
            "attempt_id": "attempt.demo.001",
            "kb_ref": "demo",
            "queue_id": "proofq.demo.001",
            "status": "in_progress",
        },
        "target": {
            "title": "Witness family transport theorem",
            "bridge_id": "bridge.001",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt",
            "candidate_object": "Witness family",
            "preserved_invariant": "witness complexity profile",
            "missing_route_lemma": "Witness-family transport lemma",
            "conjecture_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
            "route_synopsis": "Move from st.src to st.tgt through a Witness family...",
        },
        "local_context": {
            "source_excerpt": "Source theorem excerpt.",
            "target_excerpt": "Target theorem excerpt.",
        },
        "proof_attempt": {
            "theorem_statement": "There exists an admissible Witness family transporting the source lower bound to the target theorem.",
            "stepwise_argument": [{"step": 1, "claim": "Assume the Witness family exists.", "justification": "Proof scaffold."}],
        },
        "final_assessment": {"outcome": "in_progress", "summary": ""},
    }
    attempt_json = attempts_dir / "attempt.demo.001.json"
    attempt_md = attempts_dir / "attempt.demo.001.md"
    attempt_json.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    attempt_md.write_text(render_attempt_markdown(attempt), encoding="utf-8")

    report = refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        queue=queue,
    )

    refreshed_attempt = json.loads(attempt_json.read_text(encoding="utf-8"))
    assert refreshed_attempt["metadata"]["status"] == "blocked"
    assert refreshed_attempt["final_assessment"]["outcome"] == "blocked"
    assert refreshed_attempt["target"]["route_synopsis"] == "Move from st.src to st.tgt by constructing a Witness family that preserves the witness profile."
    assert report["diagnosis_overview"]["attempts_active"]["count"] == 0


def test_high_value_terminal_result_generates_produced_paper(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    attempt = {
        "metadata": {"attempt_id": "attempt.demo.003", "queue_id": "proofq.demo.003"},
        "target": {
            "bridge_id": "bridge.003",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt",
            "candidate_object": "Witness family",
            "carrier_kind": "family of hard instances",
            "preserved_invariant": "witness complexity profile",
            "route_synopsis": "Transport a lower bound through a witness family.",
            "missing_route_lemma": "The witness family amplifies the source lower bound into the target separation.",
            "conjecture_statement": "An admissible witness family transports the source lower bound to the target separation.",
            "source_excerpt": "Source theorem excerpt.",
            "target_excerpt": "Target theorem excerpt.",
            "proof_obligations": ["Realize the witness family from the source theorem."],
            "candidate_lemmas": ["The witness family preserves the witness complexity profile."],
            "negative_route": "The witness family might fail to encode the source hardness.",
            "conditional_proposition": "If the witness family exists, the target consequence follows.",
        },
        "local_context": {
            "source_excerpt": "Source theorem excerpt.",
            "target_excerpt": "Target theorem excerpt.",
        },
        "proof_attempt": {
            "strategy": "invariant-lift-through-intermediate-object",
            "assumptions": ["Assume the admissible witness family exists."],
            "local_results_used": ["mathlib.demo.010"],
            "stepwise_argument": [
                {
                    "step": 1,
                    "claim": "The source lower bound induces a witness family.",
                    "justification": "Use the source theorem and the admissibility conditions.",
                    "depends_on": ["st.src"],
                },
                {
                    "step": 2,
                    "claim": "The witness family preserves the witness complexity profile.",
                    "justification": "Apply the invariant-preservation lemma.",
                    "depends_on": ["mathlib.demo.010"],
                },
            ],
            "negative_argument": {
                "obstruction_candidate": "The witness family could be only a relabeling.",
                "counterexample_or_barrier": "No such relabeling survives the admissibility conditions.",
                "effect_on_claim": "The negative route is blocked.",
            },
        },
        "critique_judges": [
            {"title": "Statement Grounding Judge", "verdict": "pass", "notes": ["Statement matches the queue item."], "blocking_issues": []},
            {"title": "Inferential Validity Judge", "verdict": "pass", "notes": ["Each step names its dependency."], "blocking_issues": []},
        ],
        "final_assessment": {
            "summary": "This establishes a standalone transport theorem on the magnification route.",
            "novelty_assessment": "No local prior art duplicates the route-specific transport theorem.",
            "confidence": "medium",
            "verdict": "proved",
        },
        "web_search_gate": {"sources": []},
        "external_references": [],
        "major_subresult_assessment": {
            "mandatory_gates": {
                "self_contained_statement": True,
                "mathematical_inspectability": True,
                "nontrivial_frontier_relation": True,
                "independent_value": True,
            },
            "axes": {
                "frontier_shift": 3,
                "independence": 3,
                "transferability": 2,
                "barrier_clarity": 1,
                "proof_closure": 2,
                "search_compression": 1,
            },
            "justifications": {
                "frontier_shift": "The result turns a route obligation into a standalone transport theorem.",
                "independence": "Experts could inspect and reuse the transport theorem without the full P vs NP programme.",
                "transferability": "The witness-family mechanism is reusable across neighboring magnification routes.",
                "barrier_clarity": "The negative route is explicit.",
                "proof_closure": "The informal proof package is complete modulo standard verification.",
                "search_compression": "This collapses several witness-family variants into one route theorem.",
            },
            "overall_judgment": "This is paper-worthy as a standalone intermediate route theorem.",
            "paper_candidate_title": "A Witness-Family Transport Theorem for Hardness Magnification",
            "paper_candidate_summary": "A high-value intermediate result establishes a reusable transport theorem along the current magnification route.",
        },
    }
    result = {
        "result_id": "mathlib.demo.003",
        "queue_id": "proofq.demo.003",
        "attempt_id": "attempt.demo.003",
        "title": "Witness family transport theorem",
        "statement": "The witness family transports the source lower bound to the target separation.",
        "summary": "This establishes a standalone transport theorem on the magnification route.",
        "outcome": "proved",
    }

    normalized = _normalize_major_subresult_assessment(attempt)
    assert normalized["qualifies"] is True
    assert normalized["score_total"] == 12

    updated = _maybe_generate_produced_paper(
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        attempt=attempt,
        target=attempt["target"],
        result=result,
        compile_result_pdf=False,
        latex_engine="auto",
    )
    assert updated["qualifies"] is True
    assert result["produced_paper_tex"].endswith(".tex")
    tex_path = Path(result["produced_paper_tex"])
    assert tex_path.exists()
    tex_content = tex_path.read_text(encoding="utf-8")
    assert "A Witness-Family Transport Theorem for Hardness Magnification" in tex_content
    assert "Major Subresult Assessment" in tex_content
    assert "\\section{Introduction}" in tex_content
    assert "\\section{References}" in tex_content


def test_external_references_are_imported_into_mathlib(tmp_path: Path) -> None:
    mathlib = default_mathlib(kb_ref="demo")
    attempt = {
        "metadata": {"attempt_id": "attempt.demo.002", "queue_id": "proofq.demo.002"},
        "external_references": [
            {
                "reference_type": "theorem",
                "title": "Known External Theorem",
                "statement": "Every object of the required kind satisfies the transfer property.",
                "source_name": "Example Paper",
                "source_url": "https://example.org/theorem",
                "search_query": "known external theorem transfer property",
                "used_for": "Supports step 2 of the informal proof.",
                "notes": "Imported from external prior art.",
            }
        ],
    }
    target = {
        "bridge_id": "bridge.002",
        "source_statement_id": "st.src",
        "target_statement_id": "st.tgt",
    }

    imported = _persist_external_references(
        repo_root=tmp_path,
        kb_ref="demo",
        mathlib=mathlib,
        attempt=attempt,
        target=target,
    )
    assert len(imported) == 1
    assert mathlib["metadata"]["external_reference_count"] == 1
    assert mathlib["results"][0]["entry_kind"] == "external-reference"
    assert mathlib["results"][0]["reference_type"] == "theorem"

    hits = search_mathlib(mathlib, ["Known External Theorem", "transfer property"], limit=3)
    assert len(hits) == 1
    assert hits[0]["title"] == "Known External Theorem"

    report = build_summary(kb_ref="demo", queue=default_queue(kb_ref="demo"), mathlib=mathlib)
    assert report["metadata"]["external_reference_count"] == 1
    summary_markdown = render_markdown(report)
    assert "## External References" in summary_markdown
    assert "Known External Theorem" in summary_markdown


def test_finalize_blocked_attempt_persists_negative_local_theorem_into_mathlib(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.001|st.tgt|route-conjecture",
                "title": "Witness family blocked route",
                "priority": 0.91,
                "bridge_id": "bridge.001",
                "claim_type": "route-conjecture",
                "claim_text": "There exists an admissible Witness family such that the source theorem reaches the target theorem.",
                "conjecture_statement": "There exists an admissible Witness family such that the source theorem reaches the target theorem.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Witness family",
                "preserved_invariant": "witness complexity profile",
                "missing_route_lemma": "Prove the witness family transfers the lower bound to the target.",
            }
        ],
    )
    save_proof_queue(
        queue,
        json_path=artifacts_dir / "proof-queue.json",
        md_path=artifacts_dir / "proof-queue.md",
    )

    mathlib = default_mathlib(kb_ref="demo")
    mathlib_json = repo_root / "InformalMathLib" / "demo" / "index.json"
    mathlib_md = repo_root / "InformalMathLib" / "demo" / "catalog.md"
    save_high_reward_watch(
        default_high_reward_watch(kb_ref="demo"),
        json_path=artifacts_dir / "high-reward-watch.json",
        md_path=artifacts_dir / "high-reward-watch.md",
    )
    mathlib_json.parent.mkdir(parents=True, exist_ok=True)
    mathlib_json.write_text("{}", encoding="utf-8")
    mathlib_md.write_text("", encoding="utf-8")
    save_mathlib_index(mathlib, json_path=mathlib_json, md_path=mathlib_md)

    attempt_json = artifacts_dir / "proof-attempts" / "attempt.demo.001.json"
    attempt_md = artifacts_dir / "proof-attempts" / "attempt.demo.001.md"
    attempt_json.parent.mkdir(parents=True, exist_ok=True)
    attempt = {
        "metadata": {
            "attempt_id": "attempt.demo.001",
            "queue_id": "proofq.demo.001",
            "status": "in_progress",
        },
        "target": {
            "title": "Witness family blocked route",
            "bridge_id": "bridge.001",
            "source_statement_id": "st.src",
            "target_statement_id": "st.tgt",
            "candidate_object": "Witness family",
            "preserved_invariant": "witness complexity profile",
            "conjecture_statement": "There exists an admissible Witness family such that the source theorem reaches the target theorem.",
        },
        "proof_attempt": {
            "theorem_statement": "There exists an admissible Witness family such that the source theorem reaches the target theorem.",
            "result_statement": "No admissible Witness family currently realizes the source theorem in a way that preserves the witness complexity profile strongly enough to reach the target theorem.",
            "result_summary": "The route is locally blocked by the missing carrier-realization theorem.",
            "negative_argument": {
                "effect_on_claim": "The route remains blocked until the carrier-realization theorem is proved.",
            },
        },
        "final_assessment": {
            "summary": "The route is locally blocked by the missing carrier-realization theorem.",
        },
        "critique_judges": [],
    }
    attempt_json.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    attempt_md.write_text("# Attempt\n\nBlocked by a carrier-realization gap.\n", encoding="utf-8")
    monkeypatch.setattr(
        finalize_proof_cycle_module,
        "proof_queue_paths",
        lambda _repo_root, _kb_ref: (artifacts_dir / "proof-queue.json", artifacts_dir / "proof-queue.md"),
    )
    monkeypatch.setattr(
        finalize_proof_cycle_module,
        "mathlib_paths",
        lambda _repo_root, _kb_ref: (mathlib_json, mathlib_md),
    )

    original_argv = sys.argv[:]
    try:
        sys.argv = [
            "finalize_proof_cycle.py",
            "--kb-ref",
            "demo",
            "--artifacts-dir",
            str(artifacts_dir),
            "--attempt-json",
            str(attempt_json),
            "--queue-json",
            str(artifacts_dir / "proof-queue.json"),
            "--mathlib-json",
            str(mathlib_json),
            "--outcome",
            "blocked",
        ]
        assert finalize_proof_cycle_main() == 0
    finally:
        sys.argv = original_argv

    loaded_mathlib = load_mathlib_index(mathlib_json, kb_ref="demo")
    negative_results = [
        row for row in loaded_mathlib["results"] if row.get("entry_kind") == "negative-local-theorem"
    ]
    assert len(negative_results) == 1
    assert negative_results[0]["outcome"] == "blocked"
    assert "carrier-realization theorem" in negative_results[0]["summary"]

    report = build_summary(
        kb_ref="demo",
        queue=load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref="demo"),
        mathlib=loaded_mathlib,
    )
    assert report["metadata"]["blocked_count"] >= 1
    assert loaded_mathlib["metadata"]["negative_result_count"] == 1


def test_summary_refresh_backfills_historical_blocked_attempts_into_mathlib(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    queue = default_queue(kb_ref="demo")
    enqueue_entries(
        queue,
        [
            {
                "queue_key": "bridge.002|st.tgt|route-conjecture",
                "title": "Historical blocked route",
                "priority": 0.88,
                "bridge_id": "bridge.002",
                "claim_type": "route-conjecture",
                "claim_text": "Historical blocked route conjecture.",
                "conjecture_statement": "Historical blocked route conjecture.",
                "source_statement_id": "st.src",
                "target_statement_id": "st.tgt",
                "candidate_object": "Obstruction family",
                "preserved_invariant": "obstruction invariant",
                "missing_route_lemma": "Historical route lemma.",
                "status": "blocked",
            }
        ],
    )
    save_proof_queue(queue, json_path=artifacts_dir / "proof-queue.json", md_path=artifacts_dir / "proof-queue.md")

    mathlib = default_mathlib(kb_ref="demo")
    mathlib_json = repo_root / "InformalMathLib" / "demo" / "index.json"
    mathlib_md = repo_root / "InformalMathLib" / "demo" / "catalog.md"
    save_mathlib_index(mathlib, json_path=mathlib_json, md_path=mathlib_md)

    attempt_json = artifacts_dir / "proof-attempts" / "attempt.demo.002.json"
    attempt_json.parent.mkdir(parents=True, exist_ok=True)
    attempt_json.write_text(
        json.dumps(
            {
                "metadata": {
                    "attempt_id": "attempt.demo.002",
                    "queue_id": "proofq.demo.001",
                    "status": "blocked",
                },
                "target": {
                    "title": "Historical blocked route",
                    "bridge_id": "bridge.002",
                    "source_statement_id": "st.src",
                    "target_statement_id": "st.tgt",
                    "candidate_object": "Obstruction family",
                    "preserved_invariant": "obstruction invariant",
                    "conjecture_statement": "Historical blocked route conjecture.",
                },
                "proof_attempt": {
                    "result_statement": "No admissible obstruction family currently realizes the route.",
                    "result_summary": "Historical blocked attempt backfilled into InformalMathLib.",
                },
                "final_assessment": {
                    "outcome": "blocked",
                    "summary": "Historical blocked attempt backfilled into InformalMathLib.",
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    attempt_json.with_suffix(".md").write_text("# Historical Attempt\n", encoding="utf-8")

    report = refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        queue=queue,
        mathlib=mathlib,
    )

    loaded_mathlib = load_mathlib_index(mathlib_json, kb_ref="demo")
    negative_results = [row for row in loaded_mathlib["results"] if row.get("entry_kind") == "negative-local-theorem"]
    assert len(negative_results) == 1
    assert negative_results[0]["attempt_id"] == "attempt.demo.002"
    assert report["metadata"]["blocked_count"] >= 1


def test_high_reward_followups_seed_queue_and_discovery_branch(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifacts_dir = repo_root / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    queue = default_queue(kb_ref="demo")
    result = {
        "result_id": "mathlib.demo.010",
        "title": "Witness family transport theorem",
        "statement": "The witness family transports the source lower bound to the target separation.",
        "summary": "A reusable transport theorem now exists.",
    }
    target = {
        **_bridge(),
        "candidate_object": "Witness family",
        "carrier_kind": "family of hard instances",
    }
    attempt = {
        "metadata": {"attempt_id": "attempt.demo.010", "queue_id": "proofq.demo.010"},
    }

    follow_up_queue_ids, follow_up_branch_ids = _seed_high_reward_followups(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref="demo",
        queue=queue,
        result=result,
        target=target,
        attempt=attempt,
        outcome="proved",
        signal_id="highreward.demo.001",
    )

    assert len(follow_up_queue_ids) == 1
    seeded_entry = next(
        row for row in queue["entries"] if row["queue_id"] == follow_up_queue_ids[0]
    )
    assert seeded_entry["claim_type"] == "high-reward-followup"
    assert seeded_entry["high_reward_signal_id"] == "highreward.demo.001"
    assert seeded_entry["dependency_result_ids"] == ["mathlib.demo.010"]

    branch_state = load_discovery_branch_state(artifacts_dir / "discovery-branch-queue.json", kb_ref="demo")
    assert len(follow_up_branch_ids) == 1
    assert branch_state["metadata"]["branch_count"] == 1
    assert branch_state["branches"][0]["branch_id"] == follow_up_branch_ids[0]


def test_high_reward_watch_persists_signal_state(tmp_path: Path) -> None:
    watch = default_high_reward_watch(kb_ref="demo")
    json_path = tmp_path / "artifacts" / "demo" / "high-reward-watch.json"
    md_path = tmp_path / "artifacts" / "demo" / "high-reward-watch.md"
    watch["signals"].append(
        {
            "signal_id": "highreward.demo.001",
            "status": "pending",
            "result_id": "mathlib.demo.003",
            "title": "Witness family transport theorem",
            "major_subresult_score": 12,
            "recommended_extension_cycles": 4,
            "continuation_rationale": "A standalone transport theorem justifies bounded follow-up work.",
            "follow_up_prove_queue_ids": ["proofq.demo.050"],
            "follow_up_discovery_branch_ids": ["disclayer.demo.high-reward.witness"],
        }
    )
    save_high_reward_watch(watch, json_path=json_path, md_path=md_path)

    loaded = load_high_reward_watch(json_path, kb_ref="demo")
    assert loaded["metadata"]["signal_count"] == 1
    assert loaded["metadata"]["pending_count"] == 1
    assert "Witness family transport theorem" in md_path.read_text(encoding="utf-8")
