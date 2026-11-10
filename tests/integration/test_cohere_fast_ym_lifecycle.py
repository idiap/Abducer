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
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from cohere_fast_intake import parse_invocation
from agentic.orchestration.cohere_fast_runner import CohereFastRunner
from reasoning_trace_adapters import assemble_cohere_fast_trace
from build_public_reasoning_monitor_packet import build_packet
from generate_public_reasoning_trace_html import render
from generate_public_reasoning_trace_latex import render_tex


def load(path: str) -> dict:
    text = (ROOT / path).read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        import yaml
        return yaml.safe_load(text)


def public_event(receipt: dict, sequence: int) -> dict:
    step = receipt["step_id"]
    return {
        "event_id": receipt["receipt_id"], "run_id": receipt["run_id"], "workflow_id": "cohere_fast",
        "domain_id": "ym", "subworkflow_id": step, "sequence": sequence,
        "event_family": "validation" if step == "independent-audit" else "transformation",
        "artifact_validation_status": "integrity_valid", "claim_epistemic_status": "evidence_backed",
        "workflow_disposition": "accepted", "claim_level": "C2",
        "public_inference": {
            "question": f"What bounded change did {step} authorize?",
            "premises": [{"type": "artifact", "statement": f"Input digest {receipt['input_digest']} is bound to this run."}],
            "operator": "typed_domain_stage", "warrant": "The stage consumed a bound packet and retained the C2 ceiling.",
            "conclusion": f"{step} emitted its declared packet with continuum promotion forbidden.",
            "assumptions": ["The finite regulated fixture remains the active scope."],
            "alternatives": [{"candidate": "Claim C6 closure", "disposition": "rejected", "reason": "Continuum, OS, density, and universality obligations remain open."}],
            "falsifiers": ["A digest, target, regulator, or theory-identity mismatch invalidates the output."],
            "uncertainty": "No continuum or mass-gap conclusion is licensed.",
            "scope": {"regime": "finite regulated", "model": "YM integration fixture", "before": "stage input", "after": "bounded stage packet"},
            "trace_completeness": "complete",
        },
        "evidence": [{"relation": "supports", "path": "tests/fixtures/cohere_fast/ym/evidence.json", "artifact_type": "DomainEvidencePacket", "digest": "sha256:" + "a" * 64}],
        "authority": {"exercised": ["bounded-domain-transformation"], "absent": ["proof-acceptance", "continuum-promotion"], "prohibitions_checked": ["no finite-to-continuum promotion"]},
        "obligations": [{"requirement": "Discharge continuum, OS, density, and universality links.", "status": "open"}],
    }


def test_enabled_vertical_slice_executes_consumes_and_renders(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    activation = parse_invocation("cohere-fast ym", target="yang-mills")
    consumed = []
    def execute(child, packet):
        consumed.append((child["id"], sorted(packet)))
        return {"state": "accepted", "packet": {"artifact_type": child["return_type"], "previous": child["id"]},
                "artifacts": {f"packets/{child['id']}.json": json.dumps({"claim_level": "C2"})}}
    result = CohereFastRunner(tmp_path).run(activation, {"target": "yang-mills", "claim_level": "C0"}, execute)
    assert result["state"] == "accepted" and len(result["steps"]) == 5
    assert all(result["steps"][i]["input_digest"] != result["steps"][i-1]["input_digest"] for i in range(1, 5))
    assert len(consumed) == 5
    events = [public_event(receipt, i) for i, receipt in enumerate(result["steps"], 1)]
    trace = assemble_cohere_fast_trace(load("agentic/registries/cohere_fast_workflow_contracts.yaml"),
                                       load("agentic/registries/cohere_fast_subworkflows.yaml"), events,
                                       run_id=activation["run_id"], domain_id="ym", target="yang-mills")
    packet = build_packet(trace, load("agentic/registries/reasoning_trace_lenses.yaml"))
    assert packet["coverage"]["semantic_coverage"] == 1.0
    assert len(packet["claims"]) == 5 and all(c["epistemic_status"] == "evidence_backed" for c in packet["claims"])
    assert "continuum" in render(packet)
    assert "continuum" in render_tex(packet)


def test_quarantined_proof_stage_cannot_reach_audit_or_release(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "1")
    activation = parse_invocation("cohere-fast ym", target="yang-mills")
    seen = []
    def execute(child, packet):
        seen.append(child["id"])
        return {"state": "quarantined" if child["id"] == "derivation-and-proof" else "accepted", "packet": packet}
    result = CohereFastRunner(tmp_path).run(activation, {}, execute)
    assert result["state"] == "quarantined"
    assert seen == ["scope-and-ground", "adaptive-frontier", "derivation-and-proof"]
    assert "independent-audit" not in seen and "manuscript-release" not in seen
