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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "hooks/scripts"))

from cohere_fast_intake import parse_invocation
from cohere_fast_policy import authorize
from agentic.orchestration.cohere_fast_runner import CohereFastRunner

FIXTURE = ROOT / "tests/fixtures/cohere_fast/ym/codex_exec_scenarios.json"


def test_codex_generated_scenarios_replay_through_real_workflow(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    corpus = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for case in corpus["scenarios"]:
        activation = parse_invocation("cohere-fast ym", target=case["research_question"])
        policy = authorize({
            "activation_receipt": activation, "workflow_id": "cohere_fast", "domain_id": "ym",
            "run_id": activation["run_id"],
            "artifact_prefix": f"cohere-fast/ym/{activation['run_id']}/",
            "skill": "cohere-fast-orchestrator",
        })
        assert policy["decision"] == "accept"
        planned = {row["subworkflow_id"]: list(row["states"]) for row in case["attempts"]}
        findings = {row["subworkflow_id"]: row for row in case["attempts"]}
        calls: dict[str, int] = {}

        def execute(child, packet):
            step = child["id"]
            calls[step] = calls.get(step, 0) + 1
            states = planned[step]
            state = states[min(calls[step] - 1, len(states) - 1)]
            row = findings[step]
            return {
                "state": state,
                "packet": {
                    "artifact_type": child["return_type"], "claim_level": row["claim_level"],
                    "finding": row["finding"],
                    "limitations": case["evidence_scope"]["known_limitations"],
                },
                "artifacts": {
                    f"packets/{step}.json": json.dumps({
                        "scenario_id": case["id"], "claim_level": row["claim_level"],
                        "finding": row["finding"],
                    }, sort_keys=True)
                },
            }

        request = {
            "target": case["research_question"], "claim_level": case["initial_claim_level"],
            "evidence_scope": case["evidence_scope"],
        }
        result = CohereFastRunner(tmp_path / case["id"]).run(activation, request, execute)
        assert result["state"] == case["expected"]["final_state"]
        assert len(result["steps"]) == case["expected"]["executed_steps"]
        assert (result["steps"][-1]["step_id"] == "manuscript-release") is case["expected"]["release_reached"]
        assert all(
            Path(result["run_root"]).joinpath("receipts", f"{receipt['step_id']}.json").is_file()
            for receipt in result["steps"]
        )
        for step, states in planned.items():
            if step in calls:
                assert calls[step] == len(states)


def test_generated_scientific_prose_never_activates_workflow(monkeypatch) -> None:
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    corpus = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for case in corpus["scenarios"]:
        try:
            parse_invocation(case["research_question"], target="yang-mills")
        except ValueError as exc:
            assert "explicit cohere-fast alias required" in str(exc)
        else:
            raise AssertionError("generated scientific prose activated cohere-fast")
