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

from pathlib import Path

import pytest

from agentic.scripts.public_reasoning_trace_store import TraceStoreError, append_event


def promoted_event() -> dict:
    return {
        "event_id": "evt-promote",
        "run_id": "status-run",
        "workflow_id": "proof",
        "workflow_version": "1",
        "target": "theorem:x",
        "phase": "gate",
        "event_family": "validation",
        "claim_epistemic_status": "validated",
        "artifact_validation_status": "integrity_valid",
        "public_inference": {
            "question": "Is the claim established?",
            "premises": [],
            "operator": "validation",
            "warrant": "",
            "conclusion": "yes",
            "assumptions": [], "alternatives": [], "falsifiers": [], "uncertainty": "",
            "scope": {"regime": "", "model": "", "before": "finite", "after": "continuum"},
            "trace_completeness": "partial"
        },
        "evidence": [],
        "authority": {"exercised": [], "absent": [], "prohibitions_checked": []},
    }


def test_integrity_does_not_promote_claim_or_widen_scope(tmp_path: Path) -> None:
    with pytest.raises(TraceStoreError, match="validated claims require"):
        append_event(promoted_event(), store_root=tmp_path)
    complete = promoted_event()
    complete["public_inference"]["warrant"] = "A cited validator discharged the stated finite-to-continuum bridge."
    complete["evidence"] = [{"relation": "supports", "path": "artifacts/proof.json", "artifact_type": "ProofPacket", "external": False}]
    complete["authority"]["exercised"] = ["proof-validator"]
    assert append_event(complete, store_root=tmp_path)["claim_epistemic_status"] == "validated"

