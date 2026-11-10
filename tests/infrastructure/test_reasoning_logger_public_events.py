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

import importlib.util
import json
from pathlib import Path


def load_logger():
    path = Path(__file__).resolve().parents[2] / "skills/common/reasoning_log.py"
    spec = importlib.util.spec_from_file_location("reasoning_log_public_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ReasoningLogger


def test_logger_emits_typed_public_event_and_preserves_legacy_surface(tmp_path: Path) -> None:
    logger = load_logger()(
        "proof-agent", repo_root=tmp_path, run_id="run-public",
        workflow_id="theorem_proof_delivery", workflow_version="1.0.0",
        profile_id="route-a", target="theorem:x", step_id="formalize",
    )
    evidence_path = tmp_path / "artifacts/input.json"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text("{}")
    stored = logger.public_inference(
        question="Does the lemma discharge the obligation?",
        premises=[{"type": "artifact", "statement": "The checked lemma packet is available."}],
        operator="deductive_validation",
        warrant="The conclusion follows under the packet's declared assumptions.",
        conclusion="The finite lemma obligation is discharged.",
        alternatives=[{"candidate": "continuum theorem", "disposition": "rejected", "reason": "scope is finite"}],
        falsifiers=["A failed checker receipt"], uncertainty="No continuum transfer is claimed.",
        scope={"regime": "finite", "model": "matrix", "before": "finite", "after": "finite"},
        evidence=[{"relation": "supports", "path": evidence_path, "artifact_type": "LemmaPacket"}],
        claim_epistemic_status="evidence_backed", authority_exercised=["lemma-checker"],
        authority_absent=["continuum-transfer"], prohibitions_checked=["no-scope-widening"],
    )
    assert stored["workflow_id"] == "theorem_proof_delivery"
    assert stored["evidence"][0]["path"] == "artifacts/input.json"
    assert stored["public_inference"]["trace_completeness"] == "complete"
    surface = json.loads(logger.surface_json_path.read_text())
    assert any(row["kind"] == "public_inference" for row in surface["moments"])
    assert logger.log_path.exists()


def test_logger_marks_missing_public_semantics_incomplete(tmp_path: Path) -> None:
    logger = load_logger()( "minimal-agent", repo_root=tmp_path, run_id="minimal")
    stored = logger.public_inference(question="What follows?", conclusion="Unknown")
    assert stored["public_inference"]["trace_completeness"] == "trace_incomplete"
