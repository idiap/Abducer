# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for process-graph generation, agent typing, and run selection.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCH_SCRIPTS = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts"
if str(ORCH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCH_SCRIPTS))

from generate_process_graph import _build_graph
from generate_process_graph import _default_run_id_for_process_view
from generate_process_graph import _infer_agent_from_command
from generate_process_graph import _load_logs
from generate_process_graph import _parse_log


def test_process_graph_builds_typed_edges_and_states(tmp_path: Path) -> None:
    """
    Concept: Validates that process graph builds typed edges and states.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    repo = tmp_path
    artifacts_dir = repo / "artifacts" / "p-vs-np"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    log_root = repo / "artifacts" / "reasoning-logs" / "kb-orchestrator"
    log_root.mkdir(parents=True, exist_ok=True)
    out_json = artifacts_dir / "hypothesis-evaluation.json"

    content = "\n".join(
        [
            "# Reasoning Log: kb-orchestrator",
            "",
            "- Started (UTC): 2026-03-11T08:18:38.747793+00:00",
            "- Run ID: run-1",
            f"- Log file: {log_root / 'run.md'}",
            "",
            "## Step @ 2026-03-11T08:18:38.750764+00:00",
            "",
            "- Parsed orchestrator arguments",
            "- intent=hypothesis-eval",
            "- kb=KB/p-vs-np.kb.md",
            f"- artifacts_dir={artifacts_dir}",
            "",
            "## Step @ 2026-03-11T08:18:38.750829+00:00",
            "",
            "- Running stage: hypothesis-eval",
            "- command=/usr/bin/python3 /tmp/repo/skills/evaluation/kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py --output-json artifacts/p-vs-np/hypothesis-evaluation.json",
            "",
            "## Step @ 2026-03-11T08:18:38.907944+00:00",
            "",
            "- Completed stage: hypothesis-eval",
            f"- Output: hypothesis_evaluation_json -> {out_json}",
            "",
            "## Run Result",
            "",
            "- Status: success",
            "- Ended (UTC): 2026-03-11T08:18:38.908020+00:00",
            "- Duration (s): 0.160",
            "- Summary: Intent `hypothesis-eval` completed.",
            "",
            "## Declared Outputs",
            "",
            f"- hypothesis_evaluation_json: {out_json}",
            "",
        ]
    )
    (log_root / "run.md").write_text(content, encoding="utf-8")

    logs = _load_logs(
        log_root=repo / "artifacts" / "reasoning-logs",
        repo_root=repo,
        artifacts_dir=artifacts_dir,
        kb_filter="KB/p-vs-np.kb.md",
        run_id_filter="",
        include_agents=set(),
        exclude_agents=set(),
    )
    assert len(logs) == 1

    graph = _build_graph(logs, repo_root=repo)
    edge_types = {e["edge_type"] for e in graph["edges"]}
    assert "executed_by" in edge_types
    assert "has_step" in edge_types
    assert "stage_started" in edge_types
    assert "stage_completed" in edge_types
    assert "invokes_agent" in edge_types
    assert "emits_output" in edge_types or "declares_output" in edge_types
    assert len(graph["states"]) >= 4


def test_process_graph_maps_orchestrator_utility_scripts_to_agents() -> None:
    """
    Concept: Validates that process graph maps orchestrator utility scripts to agents.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    cmd_graph = "/usr/bin/python3 /tmp/repo/skills/orchestration/kb-orchestrator/scripts/generate_process_graph.py --artifacts-dir artifacts/p-vs-np"
    cmd_dynamics = "/usr/bin/python3 /tmp/repo/skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py --artifacts-dir artifacts/p-vs-np"
    assert _infer_agent_from_command(cmd_graph) == "kb-process-graph-visualizer"
    assert _infer_agent_from_command(cmd_dynamics) == "kb-reasoning-dynamics"


def test_default_run_prefers_latest_end_to_end_orchestrator_run(tmp_path: Path) -> None:
    """
    Concept: Validates that default run prefers laend to end orchestrator run.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    repo = tmp_path
    artifacts_dir = repo / "artifacts" / "p-vs-np"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    orchestration_logs = repo / "artifacts" / "reasoning-logs" / "kb-orchestrator"
    child_logs = repo / "artifacts" / "reasoning-logs" / "kb-interpretation-reporter"
    orchestration_logs.mkdir(parents=True, exist_ok=True)
    child_logs.mkdir(parents=True, exist_ok=True)

    end_to_end = "\n".join(
        [
            "# Reasoning Log: kb-orchestrator",
            "",
            "- Started (UTC): 2026-03-11T09:00:00+00:00",
            "- Run ID: run-e2e",
            "- Log file: /tmp/run-e2e.md",
            "",
            "## Step @ 2026-03-11T09:00:00+00:00",
            "",
            "- Parsed orchestrator arguments",
            "- intent=pipeline",
            "- kb=KB/p-vs-np.kb.md",
            f"- artifacts_dir={artifacts_dir}",
            "",
            "## Run Result",
            "",
            "- Status: success",
            "- Ended (UTC): 2026-03-11T09:01:00+00:00",
            "- Summary: Intent `pipeline` completed.",
            "",
        ]
    )
    (orchestration_logs / "run-e2e.md").write_text(end_to_end, encoding="utf-8")

    non_e2e_newer = "\n".join(
        [
            "# Reasoning Log: kb-interpretation-reporter",
            "",
            "- Started (UTC): 2026-03-11T09:05:00+00:00",
            "- Run ID: run-child",
            "- Log file: /tmp/run-child.md",
            "",
            "## Step @ 2026-03-11T09:05:00+00:00",
            "",
            "- Parsed report arguments",
            "- kb=KB/p-vs-np.kb.md",
            f"- artifacts_dir={artifacts_dir}",
            "",
            "## Run Result",
            "",
            "- Status: success",
            "- Ended (UTC): 2026-03-11T09:06:00+00:00",
            "- Summary: Interpretation report generated.",
            "",
        ]
    )
    (child_logs / "run-child.md").write_text(non_e2e_newer, encoding="utf-8")

    logs = [
        _parse_log(orchestration_logs / "run-e2e.md"),
        _parse_log(child_logs / "run-child.md"),
    ]
    selected, mode = _default_run_id_for_process_view(logs)
    assert selected == "run-e2e"
    assert mode == "latest-end-to-end"


def test_default_run_falls_back_to_latest_orchestrator_run(tmp_path: Path) -> None:
    """
    Concept: Validates that default run falls back to laorchestrator run.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    repo = tmp_path
    logs_dir = repo / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    older_orchestrator = "\n".join(
        [
            "# Reasoning Log: kb-orchestrator",
            "",
            "- Started (UTC): 2026-03-11T09:00:00+00:00",
            "- Run ID: run-old",
            "- Log file: /tmp/run-old.md",
            "",
            "## Step @ 2026-03-11T09:00:00+00:00",
            "",
            "- Parsed orchestrator arguments",
            "- intent=reasoning-dynamics",
            "",
            "## Run Result",
            "",
            "- Status: success",
            "- Ended (UTC): 2026-03-11T09:10:00+00:00",
            "- Summary: Intent `reasoning-dynamics` completed.",
            "",
        ]
    )
    (logs_dir / "run-old.md").write_text(older_orchestrator, encoding="utf-8")

    newer_orchestrator = "\n".join(
        [
            "# Reasoning Log: kb-orchestrator",
            "",
            "- Started (UTC): 2026-03-11T09:20:00+00:00",
            "- Run ID: run-new",
            "- Log file: /tmp/run-new.md",
            "",
            "## Step @ 2026-03-11T09:20:00+00:00",
            "",
            "- Parsed orchestrator arguments",
            "- intent=reasoning-dynamics",
            "",
            "## Run Result",
            "",
            "- Status: success",
            "- Ended (UTC): 2026-03-11T09:30:00+00:00",
            "- Summary: Intent `reasoning-dynamics` completed.",
            "",
        ]
    )
    (logs_dir / "run-new.md").write_text(newer_orchestrator, encoding="utf-8")

    latest_child = "\n".join(
        [
            "# Reasoning Log: kb-reasoning-dynamics",
            "",
            "- Started (UTC): 2026-03-11T09:40:00+00:00",
            "- Run ID: run-child",
            "- Log file: /tmp/run-child.md",
            "",
            "## Run Result",
            "",
            "- Status: success",
            "- Ended (UTC): 2026-03-11T09:41:00+00:00",
            "- Summary: Dynamics report generated.",
            "",
        ]
    )
    (logs_dir / "run-child.md").write_text(latest_child, encoding="utf-8")

    logs = [
        _parse_log(logs_dir / "run-old.md"),
        _parse_log(logs_dir / "run-new.md"),
        _parse_log(logs_dir / "run-child.md"),
    ]
    selected, mode = _default_run_id_for_process_view(logs)
    assert selected == "run-new"
    assert mode == "latest-orchestrator-run"


def test_parse_log_falls_back_to_filename_run_id_when_missing(tmp_path: Path) -> None:
    """
    Concept: Validates that parse log falls back to filename run id when missing.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    log_dir = tmp_path / "artifacts" / "reasoning-logs" / "kb-orchestrator"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "20260311T081746Z-15712.md"
    log_path.write_text(
        "\n".join(
            [
                "# Reasoning Log: kb-orchestrator",
                "",
                "- Started (UTC): 2026-03-11T08:17:46.629572+00:00",
                "",
                "## Run Result",
                "",
                "- Status: success",
                "- Ended (UTC): 2026-03-11T08:17:47.877807+00:00",
                "- Summary: Intent `pipeline` completed.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    parsed = _parse_log(log_path)
    assert parsed.run_id == "20260311T081746Z-15712"


def test_process_graph_infers_invoked_agent_from_reasoning_log_path(tmp_path: Path) -> None:
    """
    Concept: Validates that process graph infers invoked agent from reasoning log path.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    repo = tmp_path
    artifacts_dir = repo / "artifacts" / "p-vs-np"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    log_root = repo / "artifacts" / "reasoning-logs" / "kb-orchestrator"
    log_root.mkdir(parents=True, exist_ok=True)
    child_log = repo / "artifacts" / "reasoning-logs" / "kb-proof-connector" / "run-x.md"
    child_log.parent.mkdir(parents=True, exist_ok=True)

    content = "\n".join(
        [
            "# Reasoning Log: kb-orchestrator",
            "",
            "- Started (UTC): 2026-03-11T10:18:38.747793+00:00",
            "- Run ID: run-x",
            f"- Log file: {log_root / 'run.md'}",
            "",
            "## Step @ 2026-03-11T10:18:38.750764+00:00",
            "",
            "- Parsed orchestrator arguments",
            "- intent=connect",
            "- kb=KB/p-vs-np.kb.md",
            f"- artifacts_dir={artifacts_dir}",
            "",
            "## Step @ 2026-03-11T10:18:38.750829+00:00",
            "",
            "- Running stage: connect.analyze",
            "- command=/usr/bin/python3 -m wrapped.runner --script connector",
            "",
            "## Step @ 2026-03-11T10:18:38.907944+00:00",
            "",
            "- Completed stage: connect.analyze",
            f"- Output: connect.analyze.reasoning_log.1 -> {child_log}",
            "",
            "## Run Result",
            "",
            "- Status: success",
            "- Ended (UTC): 2026-03-11T10:18:38.908020+00:00",
            "- Duration (s): 0.160",
            "- Summary: Intent `connect` completed.",
            "",
        ]
    )
    (log_root / "run.md").write_text(content, encoding="utf-8")

    logs = _load_logs(
        log_root=repo / "artifacts" / "reasoning-logs",
        repo_root=repo,
        artifacts_dir=artifacts_dir,
        kb_filter="KB/p-vs-np.kb.md",
        run_id_filter="run-x",
        include_agents=set(),
        exclude_agents=set(),
    )
    graph = _build_graph(logs, repo_root=repo)
    invokes = [e for e in graph["edges"] if e["edge_type"] == "invokes_agent" and e.get("label") == "kb-proof-connector"]
    assert invokes
    assert any((e.get("meta") or {}).get("inferred_from") == "reasoning_log_path" for e in invokes)
