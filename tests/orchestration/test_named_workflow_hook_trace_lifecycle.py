# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Test optional workflow-local traces without activating them as native hooks."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
hook_utils = importlib.import_module("hooks.workflow_local.hook_utils")


def test_hook_trace_is_correlated_append_only_and_keeps_legacy_latest(tmp_path: Path, monkeypatch) -> None:
    legacy = tmp_path / "legacy"
    canonical = tmp_path / "canonical"
    monkeypatch.setattr(hook_utils, "TRACE_DIR", legacy)
    monkeypatch.setenv("ABDUCER_PUBLIC_REASONING_TRACE_ROOT", str(canonical))
    payload = {
        "run_id": "named-run",
        "workflow_id": "theorem_proof_delivery",
        "workflow_version": "1.0.0",
        "target": "theorem:x",
        "step_id": "formalize",
        "skill": "proof-obligation-formalizer",
        "attempt": 1,
        "activation_receipt": {"id": "workflow-activation-test"},
    }
    lifecycle = [
        ("user_prompt_submit_intake", {"decision": "warn", "reason": "explicit activation remains required"}),
        ("pre_skill_use_policy", {"decision": "accept", "reason": "authorized"}),
        ("pre_tool_use_policy", {"decision": "block", "reason": "deletion is prohibited"}),
        ("post_skill_use_review", {"decision": "accept", "reason": "output valid"}),
        ("stop_artifact_check", {"decision": "accept", "reason": "exit gate satisfied"}),
    ]
    for hook, result in lifecycle:
        hook_utils.trace(hook, payload, result)

    rows = [json.loads(line) for line in (canonical / "runs/named-run/events.jsonl").read_text().splitlines()]
    assert [row["event_family"] for row in rows] == ["activation", "authorization", "tool_control", "validation", "exit"]
    assert [row["sequence"] for row in rows] == [1, 2, 3, 4, 5]
    assert rows[2]["workflow_disposition"] == "blocked"
    assert rows[2]["claim_epistemic_status"] == "not_applicable"
    assert all(rows[index]["causal_parent_event_ids"] == [rows[index - 1]["event_id"]] for index in range(1, 5))
    latest = json.loads((legacy / "latest-stop_artifact_check.json").read_text())
    assert latest == {"hook": "stop_artifact_check", "payload": payload, "result": lifecycle[-1][1]}


def test_reasoned_conditional_skip_is_visible_without_epistemic_promotion(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(hook_utils, "TRACE_DIR", tmp_path / "legacy")
    monkeypatch.setenv("ABDUCER_PUBLIC_REASONING_TRACE_ROOT", str(tmp_path / "canonical"))
    payload = {
        "run_id": "skip-run", "workflow_id": "deep_review_and_reorientation",
        "workflow_version": "1.0.0", "target": "paper:x", "step_id": "synthesis",
        "skill": "review-synthesizer", "skipped_steps": [{"step_id": "optional-domain-review", "reason": "No domain-specific claim is present."}],
    }
    hook_utils.trace("pre_skill_use_policy", payload, {"decision": "accept", "reason": "authorized"})
    rows = [json.loads(line) for line in (tmp_path / "canonical/runs/skip-run/events.jsonl").read_text().splitlines()]
    assert rows[-1]["event_family"] == "skip"
    assert rows[-1]["workflow_disposition"] == "skipped"
    assert rows[-1]["claim_epistemic_status"] == "not_applicable"
    assert rows[-1]["public_inference"]["warrant"] == "No domain-specific claim is present."
