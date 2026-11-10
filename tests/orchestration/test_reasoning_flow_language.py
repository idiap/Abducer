# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from agentic.orchestration.reasoning_flow_language import (
    FlowSyntaxError,
    RELATIONS,
    parse,
    parse_file,
    reasoning_codes,
    validate_relational_coherence,
)

ROOT = Path(__file__).resolve().parents[2]
FLOW_ROOT = ROOT / "agentic/reasoning_flows"
PROJECTION = ROOT / "agentic/state/reasoning_type_workflow_projections.json"


def known_workflows() -> set[str]:
    payload = json.loads(PROJECTION.read_text(encoding="utf-8"))
    projected = {row["workflow_id"] for row in payload["workflows"]}
    represented = {path.stem for path in FLOW_ROOT.glob("*.prism")}
    return projected | represented


def test_all_curated_reasoning_flows_parse_without_skill_vocabulary() -> None:
    paths = sorted(FLOW_ROOT.glob("*.prism"))
    assert len(paths) == 19
    for path in paths:
        flow = parse_file(path, known_workflows=known_workflows())
        assert flow["id"] == path.stem
        assert "E" in reasoning_codes(flow["steps"])
        checks = validate_relational_coherence(flow)
        assert checks
        text = path.read_text(encoding="utf-8")
        assert "skill" not in text.lower()


def test_language_expresses_bounded_goal_iteration_and_workflow_switch() -> None:
    flow = parse(
        """erfl 0.2
reasoning discovery {
  goal "find a discriminating candidate" -> calibrated
  steps a:A[gap->hypothesis] -assume> d:D[hypothesis->claim] -test> r:R[claim->verdict] -calibrate> e:E[claim,verdict->status]
  repeat 1..4 [a2:A[status->hypothesis2] -assume> d2:D[hypothesis2->claim2] -test> r2:R[claim2->verdict2] -calibrate> e2:E[claim2,verdict2->status2]] until e2.promotable measure discrimination
  on e.promotable => accept
  on e.stalled => switch @conceptual_frontier_deepening
}
""",
        known_workflows={"conceptual_frontier_deepening"},
    )
    assert flow["repeats"][0]["max"] == 4
    assert flow["handlers"][-1]["action"] == "switch @conceptual_frontier_deepening"
    assert validate_relational_coherence(flow)


def test_long_routes_support_explicit_newline_continuation_and_indentation() -> None:
    multiline = parse(
        """erfl 0.3
reasoning readable_route {
  goal "calibrate a long route" -> reviewed
  steps a:A[gap->hypothesis] -assume> ...
        d:D[hypothesis->claim] -test> ...
          r:R[claim->verdict] -calibrate> ...
        e:E[claim,verdict->status]
  on e.reviewed => accept
}
"""
    )
    single_line = parse(
        """erfl 0.3
reasoning readable_route {
  goal "calibrate a long route" -> reviewed
  steps a:A[gap->hypothesis] -assume> d:D[hypothesis->claim] -test> r:R[claim->verdict] -calibrate> e:E[claim,verdict->status]
  on e.reviewed => accept
}
"""
    )
    assert multiline == single_line
    assert validate_relational_coherence(multiline)


def test_dangling_newline_continuation_fails_closed() -> None:
    with pytest.raises(FlowSyntaxError, match="dangling"):
        parse("erfl 0.3 ...")


def test_structured_goal_preserves_critic_criteria_and_obligations() -> None:
    flow = parse(
        """erfl 0.3
reasoning critical_review {
  goal {
    summary "subject the candidate to explicit criticism"
    target critically_calibrated
    criterion validity "Every inference follows from its stated premises."
    criterion alternatives "The strongest live alternative is tested."
    evidence audit_trace "The verdict is linked to claim-level evidence."
    constraint no_laundering "A not-refuted result is not a proof."
    satisfy all(validity,alternatives)
  }
  steps r:R[candidate->verdict] -calibrate> e:E[candidate,verdict->status]
  on e.critically_calibrated => accept
  on e.refuted => stop
}
"""
    )
    assert flow["goal"]["target_state"] == "critically_calibrated"
    assert [row["id"] for row in flow["goal"]["criteria"]] == ["validity", "alternatives"]
    assert flow["goal"]["evidence"][0]["id"] == "audit_trace"
    assert flow["goal"]["constraints"][0]["id"] == "no_laundering"
    assert flow["goal"]["satisfaction"] == {
        "operator": "all", "criteria": ["validity", "alternatives"],
    }
    assert validate_relational_coherence(flow)


def test_knowledge_base_is_a_first_class_versioned_object() -> None:
    flow = parse(
        """erfl 0.3
knowledge kb at "KB/problem.kb.md" access read_write persist versioned
reasoning kb_review {
  goal "calibrate a claim against the explicit KB" -> reviewed
  steps r:R[kb,candidate->verdict] -calibrate> e:E[candidate,verdict->status]
  on e.reviewed => accept
  on e.refuted => stop
}
"""
    )
    assert flow["knowledge_bases"] == [{
        "id": "kb", "ref": "KB/problem.kb.md",
        "access": "read_write", "persistence": "versioned",
    }]


def test_workflow_can_reference_read_and_persist_one_specific_kb() -> None:
    flow = parse(
        """erfl 0.3
knowledge kb at "KB/problem.kb.md" access read_write persist versioned
reasoning kb_writeback {
  goal "read and update the problem KB" -> persisted
  steps e:E[kb,proposal->status]
  on e.persisted => accept
}
"""
    )
    assert flow["knowledge_bases"] == [{
        "id": "kb", "ref": "KB/problem.kb.md",
        "access": "read_write", "persistence": "versioned",
    }]

    with pytest.raises(FlowSyntaxError, match="read-only"):
        parse(
            """erfl 0.3
knowledge kb at "KB/problem.kb.md" access read persist versioned
reasoning bad_kb {
  goal "invalid persistence" -> done
  steps e:E[kb->status]
  on e.done => accept
}
"""
        )


def test_external_kb_query_and_persistence_edges_are_directional() -> None:
    flow = parse(
        """erfl 0.3
@KB kb0 connect(file("KB/problem.kb.md"))
reasoning kb_edges {
  goal "query and persist a calibrated KB successor" -> persisted
  steps r:R[kb0,proposal->verdict] -calibrate> e:E[proposal,verdict->status]
  r <-query- kb0
  e -persist-> kb0
  on e.persisted => accept
}
"""
    )
    assert flow["knowledge_bases"] == [{
        "id": "kb0", "ref": "KB/problem.kb.md", "connector": "file",
    }]
    assert [row["operation"] for row in flow["kb_interactions"]] == ["query", "persist"]
    assert validate_relational_coherence(flow)

    invalid = flow.copy()
    invalid["kb_interactions"] = [{
        "occurrence": "r", "operation": "persist", "kb": "kb0", "direction": "write",
    }]
    with pytest.raises(FlowSyntaxError, match="calibrated E"):
        validate_relational_coherence(invalid)


def test_reflective_and_meta_reasoning_are_explicit_higher_order_compositions() -> None:
    reflective = parse(
        """erfl 0.3
reasoning reflective_route_review {
  goal "explain a stalled route and propose a bounded repair" -> reflected
  steps e0:E[trace,claims,obligations->self_model] -revise> a0:A[self_model->repair] -calibrate> e1:E[self_model,repair->reflection_status]
  on e1.reflected => accept
}
"""
    )
    assert reasoning_codes(reflective["steps"]) == ["E", "A", "E"]
    assert validate_relational_coherence(reflective)

    meta = parse(
        """erfl 0.3
@KB kb0 connect(file("KB/problem.kb.md"))
reasoning meta_strategy_review {
  goal "select or stop the current strategy" -> governed
  steps e0:E[kb0,portfolio,trace->strategy_state] -constrain> (r0:R[strategy_state->defeaters] & a0:A[strategy_state->repairs]) -calibrate> e1:E[defeaters,repairs->meta_status]
  e0 <-search- kb0
  e1 -persist-> kb0
  on e1.strategy_selected => accept
}
"""
    )
    assert reasoning_codes(meta["steps"]) == ["E", "R", "A", "E"]
    assert validate_relational_coherence(meta)


def test_declared_knowledge_base_must_be_consumed() -> None:
    source = """erfl 0.3
knowledge kb at "KB/problem.kb.md" access read persist none
reasoning unused_kb {
  goal "review" -> reviewed
  steps e:E[candidate->status]
  on e.reviewed => accept
}
"""
    with pytest.raises(FlowSyntaxError, match="not consumed"):
        parse(source)


@pytest.mark.parametrize(
    "goal_body, message",
    [
        ('target reviewed\n    satisfy all(missing)', "at least one criterion"),
        ('target reviewed\n    criterion sound \"sound\"\n    satisfy all(missing)', "unknown criteria"),
        ('target reviewed\n    criterion sound \"sound\"', "explicit satisfy"),
    ],
)
def test_structured_goal_fails_closed(goal_body: str, message: str) -> None:
    source = f"""erfl 0.3
reasoning bad_goal {{
  goal {{
    {goal_body}
  }}
  steps e:E[input->status]
  on e.reviewed => accept
}}
"""
    with pytest.raises(FlowSyntaxError, match=message):
        parse(source)


@pytest.mark.parametrize(
    "source, message",
    [
        (
            """erfl 0.2
reasoning unsafe {
  goal "iterate without a finite safety bound" -> done
  steps a:A[x->h] -test> r:R[h->v] -calibrate> e:E[h,v->s]
  repeat 1..21 [a2:A[s->h2] -test> r2:R[h2->v2] -calibrate> e2:E[h2,v2->s2]] until e2.done measure progress
  on e.done => accept
}
""",
            "repeat bounds",
        ),
        (
            """erfl 0.2
reasoning unsafe {
  goal "omit epistemic calibration entirely" -> done
  steps a:A[x->h] -assume> d:D[h->c] -test> r:R[c->v]
  on r.done => stop
}
""",
            "calibration",
        ),
        (
            """erfl 0.2
reasoning unsafe {
  goal "switch to an undeclared workflow" -> done
  steps a:A[x->h] -test> r:R[h->v] -calibrate> e:E[h,v->s]
  on e.stalled => switch @unknown_workflow
}
""",
            "unknown workflow",
        ),
    ],
)
def test_language_rejects_unsafe_or_unresolvable_flows(source: str, message: str) -> None:
    with pytest.raises(FlowSyntaxError, match=message):
        parse(source, known_workflows=set())


def test_projection_is_reproducible_and_preserves_unknowns() -> None:
    result = subprocess.run(
        [sys.executable, "agentic/scripts/project_workflows_to_reasoning_types.py", "--check"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(PROJECTION.read_text(encoding="utf-8"))
    assert payload["executable"] is False
    assert len(payload["workflows"]) == 7
    assert all(row["projection_status"] == "degraded" for row in payload["workflows"])
    assert all(row["relational_coherence"]["status"] == "unknown" for row in payload["workflows"])
    assert all(row["gaps"]["unmapped_occurrences"] for row in payload["workflows"])
    assert any(
        row["gaps"]["ambiguous_joins"]
        for row in payload["workflows"]
        if row["workflow_id"] == "evidence_to_proof_route_onramp"
    )


def test_projection_never_invents_order_within_multi_type_skill() -> None:
    payload = json.loads(PROJECTION.read_text(encoding="utf-8"))
    compound = [
        node["type_expression"]
        for workflow in payload["workflows"]
        for node in workflow["occurrences"]
        if node["type_expression"]["kind"] == "coinstantiated_unordered"
    ]
    assert compound
    assert all("primary" in row and row["secondary"] for row in compound)


def test_relational_coherence_rejects_incompatible_relation_and_lost_handle() -> None:
    incompatible = parse(
        """erfl 0.2
reasoning bad {
  goal "launder a hypothesis into a generalization" -> done
  steps a:A[gap->hypothesis] -generalize> i:I[hypothesis->pattern] -calibrate> e:E[pattern->status]
  on e.done => accept
}
"""
    )
    with pytest.raises(FlowSyntaxError, match="incoherent"):
        validate_relational_coherence(incompatible)

    disconnected = parse(
        """erfl 0.2
reasoning bad {
  goal "drop claim identity between stages" -> done
  steps a:A[gap->hypothesis] -assume> d:D[other->claim] -calibrate> e:E[claim->status]
  on e.done => accept
}
"""
    )
    with pytest.raises(FlowSyntaxError, match="no conserved claim"):
        validate_relational_coherence(disconnected)


def test_gap_bearing_flow_is_coherent_only_as_unknown_projection() -> None:
    flow = parse_file(FLOW_ROOT / "cohere_fast.prism", known_workflows=known_workflows())
    checks = validate_relational_coherence(flow)
    assert any(row["coherence"] == "unknown_gap" for row in checks)
    switch_targets = {
        handler["action"].removeprefix("switch @")
        for handler in flow["handlers"]
        if handler["action"].startswith("switch @")
    }
    assert switch_targets
    assert all(target.startswith("cohere_fast_") for target in switch_targets)


def test_relation_registry_encodes_conservation_without_support_laundering() -> None:
    registry = json.loads(
        (ROOT / "agentic/registries/epistemic_relations.yaml").read_text(encoding="utf-8")
    )
    assert {row["id"] for row in registry["relations"]} == set(RELATIONS)
    assert "supports" not in RELATIONS
    assert set(registry["state_conservation"]) == {
        "claim_identity", "scope", "provenance", "taints",
        "claim_ceiling", "open_obligations",
    }
    requires = next(row for row in registry["relations"] if row["id"] == "requires")
    assert requires["warrant_effect"] == "none"


def test_alias_and_handler_coherence_fail_closed() -> None:
    duplicate_goal = """erfl 0.2
reasoning bad {
  goal "first" -> one
  goal "second" -> two
  steps e:E[input->status]
  on e.done => accept
}
"""
    with pytest.raises(FlowSyntaxError, match="only one goal"):
        parse(duplicate_goal)

    unreachable = parse(
        """erfl 0.2
reasoning bad {
  goal "reference an absent occurrence" -> done
  steps a:A[gap->claim] -calibrate> e:E[claim->status]
  on missing.refuted => stop
  on e.done => accept
}
"""
    )
    with pytest.raises(FlowSyntaxError, match="unknown occurrence alias"):
        validate_relational_coherence(unreachable)

    noncalibrated_accept = parse(
        """erfl 0.2
reasoning bad {
  goal "accept directly from refutation" -> done
  steps a:A[gap->claim] -test> r:R[claim->verdict] -calibrate> e:E[claim,verdict->status]
  on r.not_refuted => accept
}
"""
    )
    with pytest.raises(FlowSyntaxError, match="require a calibrated"):
        validate_relational_coherence(noncalibrated_accept)


def test_bundle_reports_unbounded_cross_workflow_cycles_without_hiding_them() -> None:
    result = subprocess.run(
        [sys.executable, "agentic/scripts/build_reasoning_flow_coherence_report.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(
        (ROOT / "agentic/state/reasoning_flow_coherence.json").read_text(encoding="utf-8")
    )
    assert report["executable"] is False
    assert report["unbounded_switch_cycles"]
    assert report["global_switch_budget"] is None
    assert "source_projection_incomplete" in report["blockers"]
    strict = subprocess.run(
        [sys.executable, "agentic/scripts/build_reasoning_flow_coherence_report.py", "--require-executable"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert strict.returncode != 0
