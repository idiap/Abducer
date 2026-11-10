# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial integrity tests, explicitly not generative content evaluations.

Small synthetic records here test whether the auditor rejects missing, detached
or fabricated evaluation evidence. Actual model outputs live in a separately
prepared run and must have independently authored semantic judgments.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.generative.workflow_content_suite import (
    EvaluationError, FIXTURES, MODE, ROOT, audit, audit_controls, digest, prepare, read,
    render_report, validate_applicability_row, validate_candidate, validate_judgment, write,
)


@pytest.fixture
def records() -> tuple[dict, dict, dict, dict]:
    packet = {
        "case_id": "case", "workflow_id": "flow", "packet_sha256": "packet",
        "scenario": {"input_facts": [{"source_id": "SOURCE"}]},
        "workflow": {"steps": [{"step_id": "derive", "skill": "deriver"}]},
    }
    rubric = {"step_dimensions": {"valid_reasoning": {}},
              "workflow_dimensions": {"coherence": {}},
              "noncompensatory_gates": {"unsupported_claim": {}}}
    candidate = {
        "case_id": "case", "workflow_id": "flow", "packet_sha256": "packet",
        "execution_mode": MODE, "author_session": "test-author",
        "steps": [{"step_id": "derive", "skill_id": "deriver", "input_refs": ["SOURCE"],
                   "content": "The two finite eigenvalues are 1 and 1/2; the nonvacuum energy is log(2)."}],
        "final": {"content": "This proves only the supplied finite model statement.",
                  "unresolved_obligations": ["No continuum transfer is supplied."]},
    }
    def assessment(dimension: str, quote: str) -> dict:
        return {"dimensions": {dimension: 2}, "gates": {"unsupported_claim": True},
                "verdict": "pass", "evidence": [{"output_quote": quote,
                    "reason": "Synthetic auditor fixture, not a real semantic judgment.",
                    "source_refs": ["SOURCE"], "dimensions": [dimension], "gates": ["unsupported_claim"]}]}
    judgment = {
        "case_id": "case", "workflow_id": "flow", "candidate_sha256": digest(candidate),
        "execution_mode": MODE, "judge_session": "test-judge",
        "steps": [{"step_id": "derive", "skill_id": "deriver",
                   **assessment("valid_reasoning", "the nonvacuum energy is log(2)")}],
        "workflow": {**assessment("coherence", "only the supplied finite model"),
                     "accepted_claims": ["Finite result"], "unresolved_obligations": ["Continuum transfer"],
                     "claim_scope": "Finite model only"},
    }
    return packet, rubric, candidate, judgment


def test_integrity_acceptance_does_not_imply_external_execution(records) -> None:
    packet, rubric, candidate, judgment = records
    assert validate_judgment(judgment, candidate, packet, rubric) == "pass"
    assert candidate["execution_mode"] == "session_content_exercise"


@pytest.mark.parametrize("mutation", [
    "missing_step", "duplicate_step", "wrong_skill", "empty_content", "unknown_input", "self_reference",
])
def test_rejects_incomplete_or_unbound_generated_content(records, mutation) -> None:
    packet, _, candidate, _ = records
    if mutation == "missing_step": candidate["steps"] = []
    if mutation == "duplicate_step": candidate["steps"] *= 2
    if mutation == "wrong_skill": candidate["steps"][0]["skill_id"] = "other"
    if mutation == "empty_content": candidate["steps"][0]["content"] = " "
    if mutation == "unknown_input": candidate["steps"][0]["input_refs"] = ["FORGED"]
    if mutation == "self_reference": candidate["steps"][0]["input_refs"] = ["derive"]
    with pytest.raises(EvaluationError): validate_candidate(candidate, packet)


@pytest.mark.parametrize("mutation", [
    "self_judge", "changed_candidate", "missing_step_judge", "fabricated_quote",
    "uncovered_dimension", "uncovered_gate", "bool_score", "hidden_failure", "unfounded_omission", "unknown_source",
])
def test_rejects_false_semantic_evaluation_evidence(records, mutation) -> None:
    packet, rubric, candidate, judgment = records
    row = judgment["steps"][0]
    if mutation == "self_judge": judgment["judge_session"] = candidate["author_session"]
    if mutation == "changed_candidate": candidate["final"]["content"] += " Different claim."
    if mutation == "missing_step_judge": judgment["steps"] = []
    if mutation == "fabricated_quote": row["evidence"][0]["output_quote"] = "The continuum theorem is proved."
    if mutation == "uncovered_dimension": row["evidence"][0]["dimensions"] = []
    if mutation == "uncovered_gate": row["evidence"][0]["gates"] = []
    if mutation == "bool_score": row["dimensions"]["valid_reasoning"] = True
    if mutation == "hidden_failure": row["gates"]["unsupported_claim"] = False
    if mutation == "unfounded_omission": row["evidence"][0]["output_quote"] = None
    if mutation == "unknown_source": row["evidence"][0]["source_refs"] = ["INVENTED-AUTHORITY"]
    with pytest.raises(EvaluationError): validate_judgment(judgment, candidate, packet, rubric)


def test_failed_step_cannot_be_averaged_away_by_whole_workflow_pass(records) -> None:
    packet, rubric, candidate, judgment = records
    judgment["steps"][0]["gates"]["unsupported_claim"] = False
    judgment["steps"][0]["verdict"] = "fail"
    assert judgment["workflow"]["verdict"] == "pass"
    assert validate_judgment(judgment, candidate, packet, rubric) == "fail"


def test_useful_partial_is_not_automatically_a_failed_proof(records) -> None:
    packet, rubric, candidate, judgment = records
    judgment["steps"][0]["dimensions"]["valid_reasoning"] = 1
    judgment["steps"][0]["verdict"] = "partial"
    assert validate_judgment(judgment, candidate, packet, rubric) == "partial"


def test_declared_dag_dependency_cannot_be_replaced_by_generic_source_citation(records) -> None:
    packet, _, candidate, _ = records
    packet["workflow"]["steps"].append({"step_id": "use", "skill": "consumer", "depends_on": ["derive"]})
    candidate["steps"].append({"step_id": "use", "skill_id": "consumer", "input_refs": ["SOURCE"],
                               "content": "Uses a purported prior derivation."})
    with pytest.raises(EvaluationError, match="DAG dependency"): validate_candidate(candidate, packet)
    candidate["steps"][-1]["input_refs"].append("derive")
    validate_candidate(candidate, packet)


def test_prepare_covers_catalog_without_leaking_oracles_or_generating_outputs(tmp_path: Path) -> None:
    manifest = prepare(tmp_path)
    catalog = read(ROOT / "agentic/registries/reasoning_flow_catalog.yaml")
    cases = read(FIXTURES / "workflow_content_cases.json")["cases"]
    assert len(manifest["case_ids"]) == len(cases) >= 2 * len(catalog["flows"])
    for workflow in catalog["flows"]:
        assert {"constructive", "adverse"} <= {case["variant"] for case in cases if case["workflow_id"] == workflow["id"]}
    for case_id in manifest["case_ids"]:
        packet = read(tmp_path / "author_packets" / f"{case_id}.json")
        assert "expected_outcomes" not in packet["scenario"]
        assert "forbidden_inferences" not in packet["scenario"]
        assert "oracle" not in packet
        assert packet["skill_instructions"]
    report = audit(tmp_path)
    assert report["evaluated_cases"] == report["evaluated_step_assessments"] == 0
    assert report["coverage_complete"] is False
    assert all(row["status"] == "unexecuted" for row in report["cases"])
    with pytest.raises(EvaluationError, match="overwrite"): prepare(tmp_path)


@pytest.mark.parametrize("surface", ["author_packets", "judge_packets"])
def test_changed_prompt_or_oracle_cannot_reuse_prepared_run(tmp_path: Path, surface: str) -> None:
    manifest = prepare(tmp_path)
    path = tmp_path / surface / f"{manifest['case_ids'][0]}.json"
    packet = read(path)
    packet["tampered"] = True
    write(path, packet)
    report = audit(tmp_path)
    assert report["coverage_complete"] is False
    assert report["cases"][0]["status"] == "invalid_evidence"


def test_missing_packet_is_reported_without_losing_expected_coverage(tmp_path: Path) -> None:
    manifest = prepare(tmp_path)
    (tmp_path / "author_packets" / f"{manifest['case_ids'][0]}.json").unlink()
    report = audit(tmp_path)
    assert report["cases"][0]["status"] == "invalid_evidence"
    workflows = {row["workflow_id"]: row for row in manifest["inventory"]["workflows"]}
    expected = sum(len(workflows[workflow_id]["steps"]) for workflow_id in manifest["case_workflows"].values())
    assert report["expected_step_assessments"] == expected
    assert not report["coverage_complete"]


def test_empty_manifest_cannot_claim_complete_coverage(tmp_path: Path) -> None:
    manifest = prepare(tmp_path)
    manifest["case_ids"] = []
    write(tmp_path / "manifest.json", manifest)
    with pytest.raises(EvaluationError, match="empty/duplicate"): audit(tmp_path)


def test_catalog_itself_is_frozen(tmp_path: Path) -> None:
    manifest = prepare(tmp_path)
    assert manifest["inventory"]["catalog_path"] in manifest["source_digests"]


def test_prepared_controls_and_answer_key_cannot_be_rewritten(tmp_path: Path) -> None:
    manifest = prepare(tmp_path)
    assert (tmp_path / "controls/packet.json").is_file()
    path = tmp_path / "controls/answer-key.json"
    key = read(path)
    key["expected"]["probe_k7"] = {"all_gates_pass": True}
    write(path, key)
    result = audit_controls(tmp_path, {"judge"}, manifest["rubric"],
                            expected_digests=manifest["control_digests"])
    assert not result["complete"]
    assert "changed" in result["reason"]


@pytest.mark.parametrize("positive_gate", [True, False])
def test_controls_reject_a_judge_that_rejects_everything(tmp_path: Path, positive_gate: bool) -> None:
    packet = {"records": [
        {"control_id": "good", "content": "A valid bounded result.", "source_facts": [{"source_id": "S"}]},
        {"control_id": "bad", "content": "An unsupported result.", "source_facts": [{"source_id": "S"}]},
    ]}
    write(tmp_path / "controls/packet.json", packet)
    write(tmp_path / "controls/answer-key.json", {"expected": {
        "good": {"all_gates_pass": True}, "bad": {"failed_gate": "unsupported_claim"}
    }})
    rows = []
    for record in packet["records"]:
        gate = positive_gate if record["control_id"] == "good" else False
        rows.append({"control_id": record["control_id"], "dimensions": {},
                     "gates": {"unsupported_claim": gate}, "verdict": "pass" if gate else "fail",
                     "evidence": [{"output_quote": record["content"], "reason": "Auditor-only control fixture.",
                                   "source_refs": ["S"], "dimensions": [], "gates": ["unsupported_claim"]}]})
    write(tmp_path / "controls/judgments/test.json", {
        "judge_session": "judge", "packet_sha256": digest(packet), "evaluations": rows
    })
    result = audit_controls(tmp_path, {"judge"}, {"noncompensatory_gates": {"unsupported_claim": "gate"}})
    assert result["complete"] is positive_gate


def test_controls_do_not_license_another_judge(tmp_path: Path) -> None:
    write(tmp_path / "controls/packet.json", {"records": []})
    write(tmp_path / "controls/answer-key.json", {"expected": {}})
    result = audit_controls(tmp_path, {"unobserved-judge"}, {"noncompensatory_gates": {}})
    assert result["complete"] is False
    assert result["missing_judges"] == ["unobserved-judge"]


def test_report_keeps_rejected_judgment_invalid_without_crashing(tmp_path: Path, records) -> None:
    packet, _, candidate, _ = records
    write(tmp_path / "author_packets/case.json", packet)
    write(tmp_path / "candidates/case.json", candidate)
    path = tmp_path / "judgments/case.json"
    path.parent.mkdir()
    path.write_text("{malformed evidence")
    report = {"evaluated_cases": 0, "case_count": 1, "evaluated_step_assessments": 0,
              "expected_step_assessments": 1, "limitations": [], "cases": [
                  {"case_id": "case", "status": "invalid_evidence", "expected_steps": 1,
                   "error": "Malformed judgment"}]}
    render_report(tmp_path, report)
    rendered = (tmp_path / "report.html").read_text()
    assert "Invalid evidence: Malformed judgment" in rendered
    assert "derive — not judged" in rendered


@pytest.mark.parametrize("status,scope", [("inactive", "guard_decision"), ("unknown", "conditional_proposal")])
def test_guard_explanation_cannot_earn_scientific_content_credit(records, status, scope) -> None:
    packet, _, candidate, _ = records
    packet["source_digests"] = {}
    binding = {"when": "premise_supplied"}
    row = {"workflow_id": "flow", "step_id": "derive", "candidate_sha256": digest(candidate),
           "condition": binding["when"], "condition_status": status, "assessment_scope": scope,
           "content_score": None, "output_quote": candidate["steps"][0]["content"],
           "source_refs": ["SOURCE"], "reason": "Auditor fixture checks null accounting only.",
           "native_execution": False}
    validate_applicability_row(row, candidate, packet, binding)
    row["content_score"] = 2
    with pytest.raises(EvaluationError, match="must be null"):
        validate_applicability_row(row, candidate, packet, binding)
