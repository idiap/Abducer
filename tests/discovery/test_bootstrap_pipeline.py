# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exercise full initialization with controlled model/HTTP boundaries.

Only the two external capabilities are replaced. Producers, typed model schemas,
repair journals, validators, both execution waves and canonical CAS are real.
The fixture's scientific prose is deliberately not evidence of a live discovery.
"""
import copy
import json
import os
from pathlib import Path
import sys

import pytest

from agentic.discovery.bootstrap_authoring import proposal_schema
from agentic.discovery.bootstrap_pipeline import initialize_canonical_theory
from agentic.discovery.bootstrap_reflection import authored_system_view
from agentic.discovery.contracts import ContractError
from agentic.discovery.reflection import system_from_hypothesis
from agentic.discovery.theory_gate import verify_canonical_theory_cycle
from tests.discovery.test_bootstrap_authoring import inputs as proposal_inputs
from tests.discovery.test_bootstrap_literature import Channel
from tests.discovery.test_canonical_discovery_cycle import (
    CanonicalExercise, _typed_unification, _conceptual_judgment,
)


def strip_derived(value):
    if isinstance(value, list):
        return [strip_derived(row) for row in value]
    if isinstance(value, dict):
        return {key: strip_derived(row) for key, row in value.items()
                if key not in {"value_digest", "analysis_digest", "dimension"}}
    return value


class ControlledModel:
    """Return deterministic scientific fixtures through the actual JSON transport."""
    def __init__(self, *, positive=True, revise_synthesis=False):
        self.calls = []
        self.positive = positive
        self.revise_synthesis = revise_synthesis

    def __call__(self, **arguments):
        task = json.loads(arguments["messages"][1]["content"])
        inputs, schema = task["inputs"], task["output_schema"]
        fields = set(schema["properties"])
        self.calls.append(fields)
        if len(arguments["messages"]) > 2:
            pytest.fail("Controlled artifact failed validation: " + arguments["messages"][-1]["content"])
        if "discovery_charter" in fields:
            fixture = object.__new__(CanonicalExercise)
            fixture.target_id, fixture.run_id, fixture.state_version, fixture.receipts = inputs["target_id"], "controlled", 0, []
            request = fixture._reflection_request({}, {}, {"snapshot_id": "snapshot", "content_digest": "digest",
                "search_completed_at": "2026-09-15T00:00:00Z", "lane_receipts": [], "coverage_limits": []}, "assimilation.json")
            value = {key: request[key] for key in fields}
            value["discovery_charter"]["target_commitments"] = inputs["commitments"]
            value["root_tensions"] *= 2
            value["root_tensions"][1] = {**value["root_tensions"][1], "tension_id": "second-tension"}
            self.genealogy = value["conceptual_genealogy"]
        elif "proposals" in fields:
            value = proposal_inputs()[2]["value"]
        elif "assessments" in fields:
            value = {"assessments": [{"source_id": row["source_id"], "relevance": "direct",
                "source_excerpt": row["claims"][0], "reason": "The finite result leaves the full target unresolved.",
                "credibility_concerns": ["Abstract-only observation is unverified."],
                "usable_for": ["Which exact assumption prevents transfer to the full target?"], "claims_verified": False}
                for row in inputs["sources"]], "coverage_limitations": ["Controlled fixture acquisition only."]}
        elif "rebases" in fields:
            value = {"rebases": [{"mechanism_key": row["mechanism_key"], "literature_relation": "coverage_unknown",
                "source_ids": [], "rationale": "No global novelty follows from this bounded acquisition.",
                "remaining_checks": ["Read complete primary arguments."]} for row in inputs["blind_proposals"]]}
        elif "theory_delta" in fields:
            value = {"theory_delta": {"delta_class": "conceptual_maturation", "changed_question": "Which exact boundary prevents the proposed transfer?",
                "mechanism": "Retain the local hypothesis with its unresolved transfer obligation.",
                "new_explanatory_dependencies": [], "new_distinctions": [],
                "blocking_gaps": ["No global derivation has been supplied."], "falsifiers": ["A boundary counterexample retires this mechanism."]},
                "claims": [], "is_dissent": False}
        elif fields == {"systems"}:
            systems = []
            for assignment, hypothesis in zip(inputs["assignments"], inputs["hypotheses"], strict=True):
                row = authored_system_view(_typed_unification(system_from_hypothesis(hypothesis, self.genealogy)))
                row["system_id"] = assignment["system_id"]
                systems.append(row)
            value = {"systems": systems}
        elif "round" in fields:
            value = {"systems": inputs["systems"], "round": {
                "round_id": inputs["round_id"], "system_ids": [row["system_id"] for row in inputs["systems"]],
                "lenses_used": ["ontological", "dialectical"],
                "strongest_objections": ["The proposed mediator still lacks a noncircular global derivation."],
                "blind_spots": ["The finite observation cannot decide the global obligation."],
                "mutation_or_synthesis": {"operation": "Retain the unresolved systems without inventing a revision.",
                    "changed_primitives_relations_or_explanation": [], "preserved_content": ["Exact target commitments remain unchanged."],
                    "lost_content": []}, "result": "no_change", "no_change_reason": "No justified conceptual revision follows from this controlled evidence."}}
        elif "panels" in fields:
            value = {"panels": [{"lens_family": lens, "findings": [
                {"candidate_alias": row["candidate_alias"], **strip_derived(_conceptual_judgment(row, inputs, lens))}
                for row in inputs["candidates"]]} for lens in ("ontological", "dialectical", "explanatory")]}
            if self.positive:
                for panel in value["panels"]:
                    for dimension in panel["findings"][0]["dimensions"].values():
                        dimension["rating"] = "strong"
        else:
            pytest.fail("Unexpected model contract: " + str(fields))
        if "round" in fields and inputs.get("sealed_critique") and self.revise_synthesis:
            value["systems"][0]["mechanism_or_principle"] += " A separate boundary witness must discharge the transfer obligation before promotion."
            value["round"].update(result="mutated", no_change_reason=None)
            value["round"]["mutation_or_synthesis"]["changed_primitives_relations_or_explanation"] = [
                "Added an explicit boundary-witness obligation to the first candidate mechanism."]
        return {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(value)}}]}


@pytest.mark.parametrize("positive,revise_synthesis", [(True, False), (False, False), (True, True)])
def test_initialization_commits_real_operator_wave_and_reuses_model_content(tmp_path, monkeypatch, positive, revise_synthesis):
    monkeypatch.setenv("PATH", str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"])
    monkeypatch.setenv("PYTHONPATH", str(Path(__file__).resolve().parents[2]))
    model, channel = ControlledModel(positive=positive, revise_synthesis=revise_synthesis), Channel()
    binding = initialize_canonical_theory(workspace=tmp_path, root=tmp_path / "initialization",
        target_id="p-vs-np-target", run_id="controlled-new-run", model_id="controlled-test-model",
        completion=model, public_fetch=channel)
    cycle = json.loads((tmp_path / binding["canonical_theory_cycle"]).read_text())
    assert len(model.calls) == 13
    assert len(channel.urls) == 6
    assert binding["scientific_truth_verified"] is False
    assert cycle["target_id"] == "p-vs-np-target"
    assert cycle["run_id"] == "controlled-new-run"
    assert (tmp_path / binding["canonical_theory_state_root"]).is_dir()
    gate = verify_canonical_theory_cycle(tmp_path / binding["canonical_theory_cycle"],
        target_id="p-vs-np-target", run_id="controlled-new-run", state_root=tmp_path / binding["canonical_theory_state_root"])
    assert gate["status"] == ("verified_active_current" if positive else "verified_active_current_no_investment")
    assert bool(gate["eligible_branch_ids"]) is positive
    seeds = json.loads((tmp_path / binding["canonical_branch_seeds"]).read_text())
    assert [row["binding"] for row in seeds["branches"]] == cycle["identity_map"]["branch_bindings"]
    # Persist the bridge in the test workspace, with real legacy branch helpers.
    # Only path roots change; no writes may reach the checkout's research state.
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[2] / "agentic/scripts"))
    import discovery_marathon_common as common
    from integrations.domain_package.marathon_runtime import initialize_marathon_branches
    monkeypatch.setattr(common, "ROOT", tmp_path)
    monkeypatch.setattr(common, "MARATHON_ROOT", tmp_path / "agentic/runs/discovery_marathons")
    monkeypatch.setattr(common, "ACTIVE_POINTER", common.MARATHON_ROOT / "active_run.json")
    monkeypatch.setattr(common, "TARGET_ACTIVE_DIR", common.MARATHON_ROOT / "active_targets")
    monkeypatch.setattr(common, "rel", lambda path: Path(path).relative_to(tmp_path).as_posix())
    state = initialize_marathon_branches(tmp_path, binding, gate)
    assert state["active_branch_ids"] == [row["binding"]["branch_id"] for row in seeds["branches"]
                                          if row["binding"]["branch_id"] in gate["eligible_branch_ids"]]
    assert state["canonical_initialization"]["research_authorized"] is positive
    for seed, row in zip(seeds["branches"], common.load_branches(state), strict=True):
        assert row["canonical_identity_binding"] == seed["binding"]
        assert row["canonical_hypothesis"] == seed["hypothesis"]
    seeds["branches"][0]["hypothesis"]["intuitive_leap"] = "tampered"
    (tmp_path / binding["canonical_branch_seeds"]).write_text(json.dumps(seeds))
    with pytest.raises(ValueError, match="exact canonical ancestor"):
        initialize_marathon_branches(tmp_path, binding, gate)
    with pytest.raises(FileExistsError):
        initialize_canonical_theory(workspace=tmp_path, root=tmp_path / "initialization",
            target_id="p-vs-np-target", run_id="controlled-new-run", model_id="controlled-test-model",
            completion=model, public_fetch=channel)
    assert len(model.calls) == 13
