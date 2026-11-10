# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from pathlib import Path

from hegelian_solver.io import read_structured


ROOT = Path(__file__).resolve().parents[2]


def test_cancer_mechanisms_area_trace_is_structured():
    payload = read_structured(
        ROOT / "hegelian_solver/examples/area_traces/cancer_mechanisms_and_therapeutics.yaml"
    )
    trace = payload["area_conceptual_trace"]

    assert trace["area"]
    assert trace["scope_note"]
    assert trace["recommended_next_step"] in {
        "retrospective_evolution_formalizer",
        "web_expansion_scout",
        "none",
    }

    key_concepts = trace["key_concepts"]
    assert len(key_concepts) >= 8

    seen_ids = set()
    for concept in key_concepts:
        assert concept["concept_id"] not in seen_ids
        seen_ids.add(concept["concept_id"])
        assert concept["name"]
        assert concept["summary"]
        assert concept["informal_evidence"]
        for evidence in concept["informal_evidence"]:
            assert evidence["claim"]
            assert evidence["source_note"]
            assert evidence["confidence"] in {"high", "medium", "low"}
            assert isinstance(evidence["web_search_used"], bool)

    # the first entry has no predecessor; every later entry should explain its own shift
    assert key_concepts[0]["shift_from_previous"] is None
    assert all(concept["shift_from_previous"] for concept in key_concepts[1:])

    # at least one searched and one un-searched claim, since the skill should triage rather
    # than search everything or nothing
    all_evidence = [item for concept in key_concepts for item in concept["informal_evidence"]]
    assert any(item["web_search_used"] for item in all_evidence)
    assert any(not item["web_search_used"] for item in all_evidence)

    assert trace["open_threads"]
    assert trace["assumptions"]
    assert trace["unknowns"]
