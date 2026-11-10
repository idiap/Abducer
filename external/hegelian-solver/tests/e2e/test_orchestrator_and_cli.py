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

from hegelian_solver.cli.main import main
from hegelian_solver.orchestrator import run_solver
from hegelian_solver.schemas import ReasoningLog
from hegelian_solver.skills_runtime.ledger import RunLedger


ROOT = Path(__file__).resolve().parents[2]


def test_orchestrator_runs_naturals_end_to_end(tmp_path):
    trace = run_solver(ROOT / "hegelian_solver/examples/naturals.yaml", output_dir=tmp_path)

    assert trace.failures
    assert trace.candidates
    assert trace.validation_packets
    assert trace.ranking_decisions
    assert trace.graph_updates["edges"]
    assert trace.reasoning_log["steps"]
    assert "candidate repair" in trace.explanation
    ledger_file = next((tmp_path / "run_ledgers").glob("*.json"))
    ledger = RunLedger.load(ledger_file)
    assert "ranking" in ledger.completed_stages()
    assert "reasoning_log" in ledger.completed_stages()
    assert ledger.resume_payload()["concept_formalization"]["name"] == "Naturals"
    log_file = next((tmp_path / "reasoning_logs").glob("*.json"))
    log = ReasoningLog.load(log_file)
    assert [step.stage for step in log.steps] == [
        "domain_profile",
        "concept_formalization",
        "task_evidence",
        "failure_classification",
        "discovery_mining",
        "candidate_generation",
        "validation",
        "ranking",
        "conceptual_creativity",
        "reflective_refinement",
        "graph_update",
        "explanation",
    ]
    assert trace.refinement["stop_reason"]
    assert trace.refinement["iterations_run"] >= 1
    assert trace.creativity_analyses
    assert all(item["source_pressure"] and item["operation"] for item in trace.creativity_analyses)
    report_file = next((tmp_path / "reports").glob("*.html"))
    report = report_file.read_text()
    assert "Hegelian Solver Report" in report
    assert "reasoning-log-json" in report
    assert 'class="summary-points"' in report
    assert "Use Case Motivation" in report
    assert "hegelian-use-case-motivation-writer" in report
    assert "Full Explanation" in report
    assert "Big Picture" in report
    assert "What Breaks" in report
    assert "How To Read The Result" in report
    assert "Conceptual Creativity Analysis" in report
    assert "id=\"creativity-analysis\"" in report
    assert "Structured creativity payload" in report
    assert "introduce a new affordance" in report
    assert "<summary>Reasoning Log</summary>" in report
    assert "Concrete Concept Evolution" in report
    assert "Source concept" in report
    assert "Formal Reasoning Notation" in report
    assert "Notation Legend" in report
    assert "tex-svg.js" in report
    assert '<details class="json-details">' in report
    assert r"\begin{aligned}" in report
    assert r"\mathcal{K}" in report


def test_fixture_suite_runs_for_required_examples(tmp_path):
    for name in [
        "naturals.yaml",
        "metric_space.yaml",
        "newtonian_mechanics.yaml",
        "assistant.yaml",
        "group_examples.yaml",
    ]:
        trace = run_solver(ROOT / f"hegelian_solver/examples/{name}", output_dir=tmp_path / name)
        assert trace.seed_nodes
        assert trace.tasks
        assert trace.candidates


def test_cli_run_and_graph_inspect(tmp_path, capsys):
    concept_file = ROOT / "hegelian_solver/examples/naturals.yaml"
    assert main(["run", str(concept_file), "--output-dir", str(tmp_path), "--human"]) == 0
    out = capsys.readouterr().out
    assert "Naturals develops" in out

    graph_file = next((tmp_path / "graphs").glob("*.json"))
    assert main(["graph", "inspect", str(graph_file)]) == 0
    out = capsys.readouterr().out
    assert '"edges"' in out


def test_cli_reasoning_log_and_report(tmp_path, capsys):
    concept_file = ROOT / "hegelian_solver/examples/naturals.yaml"
    assert main(["run", str(concept_file), "--output-dir", str(tmp_path)]) == 0
    capsys.readouterr()
    trace_file = next((tmp_path / "traces").glob("*.json"))

    assert main(["reasoning-log", str(trace_file)]) == 0
    out = capsys.readouterr().out
    assert '"stage": "domain_profile"' in out

    output = tmp_path / "custom-report.html"
    assert main(["report", str(trace_file), "--output", str(output)]) == 0
    out = capsys.readouterr().out
    assert str(output) in out
    report = output.read_text()
    assert "Use Case Motivation" in report
    assert "Full Explanation" in report
    assert "Big Picture" in report
    assert "Conceptual Creativity Analysis" in report
    assert 'class="summary-points"' in report
    assert "<summary>Reasoning Log</summary>" in report
    assert "Concrete Concept Evolution" in report
    assert "Formal Reasoning Notation" in report
    assert "Notation Legend" in report
    assert "tex-svg.js" in report
    assert '<details class="json-details">' in report


def test_cli_mechanism_commands(tmp_path, capsys):
    mechanisms_file = ROOT / "hegelian_solver/examples/mechanisms/abductive_mechanism_requirements.yaml"

    assert main(["mechanism", "dossier", str(mechanisms_file), "--id", "mechanism_clinical_transport_calibrated_evidence"]) == 0
    out = capsys.readouterr().out
    assert '"mechanism_abduction_packet"' in out
    assert '"mechanism_todo_packet"' in out

    assert main(
        [
            "mechanism",
            "dossier",
            str(mechanisms_file),
            "--id",
            "mechanism_clinical_transport_calibrated_evidence",
            "--validation-packet",
        ]
    ) == 0
    out = capsys.readouterr().out
    assert '"candidate_id": "mechanism::Transport-Calibrated Evidence Mediation"' in out
    assert '"hard_gate_failures"' in out


def test_cli_report_with_mechanisms(tmp_path, capsys):
    concept_file = ROOT / "hegelian_solver/examples/naturals.yaml"
    mechanisms_file = ROOT / "hegelian_solver/examples/mechanisms/abductive_mechanism_requirements.yaml"
    assert main(["run", str(concept_file), "--output-dir", str(tmp_path)]) == 0
    capsys.readouterr()
    trace_file = next((tmp_path / "traces").glob("*.json"))

    output = tmp_path / "report-with-mechanisms.html"
    assert main(
        ["report", str(trace_file), "--output", str(output), "--mechanisms", str(mechanisms_file)]
    ) == 0
    report = output.read_text()
    assert "Transport-Calibrated Evidence Mediation" in report
    assert "Counterfactual critique" in report
    assert "TODO backlog" in report
    assert 'class="todo-group"' in report


def test_cli_creativity_command(tmp_path, capsys):
    concept_file = ROOT / "hegelian_solver/examples/naturals.yaml"
    assert main(["run", str(concept_file), "--output-dir", str(tmp_path)]) == 0
    capsys.readouterr()
    trace_file = next((tmp_path / "traces").glob("*.json"))

    assert main(["creativity", str(trace_file)]) == 0
    out = capsys.readouterr().out
    assert '"operation"' in out
    assert '"repair_vs_affordance"' in out
    assert '"why_creative_not_corrective"' in out

    assert main(["creativity", str(trace_file), "--validate"]) == 0
    out = capsys.readouterr().out
    assert '"valid": true' in out


def test_cli_use_case_suite_commands(tmp_path, capsys):
    manifest = ROOT / "hegelian_solver/examples/use_cases/spec_use_cases.yaml"

    assert main(["list-use-cases", "--path", str(manifest)]) == 0
    out = capsys.readouterr().out
    assert '"total": 65' in out
    assert "math_number_systems" in out

    assert main(["validate-use-cases", "--path", str(manifest)]) == 0
    out = capsys.readouterr().out
    assert '"valid": true' in out

    assert main(["run-suite", "--path", str(manifest), "--output-dir", str(tmp_path), "--limit", "2"]) == 0
    out = capsys.readouterr().out
    assert '"failed": 0' in out
    assert (tmp_path / "suite_result.json").exists()
