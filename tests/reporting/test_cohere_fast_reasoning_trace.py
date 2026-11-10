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
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from agentic.discovery.contracts import validate_instance
from build_public_reasoning_monitor_packet import build_packet
from generate_public_reasoning_trace_html import render
from generate_public_reasoning_trace_latex import render_tex
from reasoning_trace_adapters import assemble_cohere_fast_trace


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def event(step: str, sequence: int, *, status: str = "evidence_backed") -> dict:
    return {
        "event_id": f"cf-live.{sequence}", "run_id": "cf-live", "workflow_id": "cohere_fast",
        "domain_id": "ym", "subworkflow_id": step, "sequence": sequence,
        "event_family": "validation" if step == "independent-audit" else "transformation",
        "artifact_validation_status": "integrity_valid", "claim_epistemic_status": status,
        "workflow_disposition": "accepted", "claim_level": "C2",
        "public_inference": {
            "question": f"What does {step} establish?",
            "premises": [{"type": "artifact", "statement": "A domain-bound input packet was validated."}],
            "operator": "bounded_domain_transformation", "warrant": "The typed input and declared claim ceiling constrain the transformation.",
            "conclusion": f"{step} produced a bounded YM packet without continuum promotion.",
            "assumptions": ["The target binding remains unchanged."],
            "alternatives": [{"candidate": "Promote to C6", "disposition": "rejected", "reason": "Continuum and OS obligations remain open."}],
            "falsifiers": ["A target or regulator mismatch invalidates the packet."],
            "uncertainty": "Continuum implications remain unproved.",
            "scope": {"regime": "finite regulated", "model": "YM fixture", "before": "domain input", "after": "bounded packet"},
            "trace_completeness": "complete",
        },
        "evidence": [{"relation": "supports", "path": "tests/fixtures/cohere_fast/ym/evidence.json", "artifact_type": "DomainEvidencePacket", "digest": "sha256:" + "a" * 64}],
        "authority": {"exercised": ["bounded-domain-assessment"], "absent": ["proof-acceptance", "continuum-promotion"], "prohibitions_checked": ["no finite-to-continuum promotion"]},
        "obligations": [{"requirement": "Prove continuum and OS reconstruction links.", "status": "open"}],
    }


def test_live_cohere_fast_trace_renders_from_one_packet() -> None:
    parent = load("agentic/registries/cohere_fast_workflow_contracts.yaml")
    children = load("agentic/registries/cohere_fast_subworkflows.yaml")
    events = [event(row["id"], i) for i, row in enumerate(children["subworkflows"], 1)]
    trace = assemble_cohere_fast_trace(parent, children, events, run_id="cf-live", domain_id="ym", target="yang-mills")
    packet = build_packet(trace, load("agentic/registries/reasoning_trace_lenses.yaml"))
    assert packet["identity"]["domain_id"] == "ym"
    assert packet["identity"]["execution_kind"] == "live"
    assert packet["coverage"]["semantic_coverage"] == 1.0
    html = render(packet)
    tex = render_tex(packet)
    assert "Cohere-fast" in html and "finite-to-continuum" in html
    assert "Cohere" in tex and "continuum" in tex


def test_synthetic_trace_cannot_present_validated_science() -> None:
    parent = load("agentic/registries/cohere_fast_workflow_contracts.yaml")
    children = load("agentic/registries/cohere_fast_subworkflows.yaml")
    synthetic = event("scope-and-ground", 1, status="validated"); synthetic["run_id"] = "fixture"
    trace = assemble_cohere_fast_trace(parent, children, [synthetic],
                                       run_id="fixture", domain_id="ym", target="yang-mills",
                                       subworkflow_id="scope-and-ground", execution_kind="synthetic_fixture")
    assert trace["events"][0]["claim_epistemic_status"] == "unknown"
    assert trace["events"][0]["trace_incomplete"] is True


def test_schema_valid_public_inference_has_semantic_coverage() -> None:
    parent = load("agentic/registries/cohere_fast_workflow_contracts.yaml")
    children = load("agentic/registries/cohere_fast_subworkflows.yaml")
    raw = event("adaptive-frontier", 1, status="conjectural")
    raw.update({
        "schema_version": "2.0.0",
        "workflow_version": "1.0.0",
        "target": "yang-mills",
        "timestamp_utc": "2026-08-06T12:00:00+00:00",
        "phase": "adaptive-frontier",
        "skill": "ym-design-regulator-atlas",
        "event_family": "public_inference",
        "execution_kind": "live",
    })
    raw["evidence"][0]["external"] = False
    raw.pop("obligations")
    raw["obligation"] = {
        "requirement": "Prove continuum and OS reconstruction links.",
        "status": "open",
    }
    validate_instance(raw, "public_reasoning_event.schema.json")
    validate_instance(
        {
            "schema_version": "2.0.0",
            "run_id": "cf-live",
            "workflow_id": "cohere_fast",
            "workflow_version": "1.0.0",
            "domain_id": "ym",
            "subworkflow_id": "adaptive-frontier",
            "execution_kind": "live",
            "target": "yang-mills",
            "status": "running",
            "events": [raw],
        },
        "public_reasoning_trace.schema.json",
    )
    trace = assemble_cohere_fast_trace(
        parent,
        children,
        [raw],
        run_id="cf-live",
        domain_id="ym",
        target="yang-mills",
        subworkflow_id="adaptive-frontier",
    )
    packet = build_packet(trace, load("agentic/registries/reasoning_trace_lenses.yaml"))
    assert trace["declared_route"][0]["inference_event_ids"] == [raw["event_id"]]
    assert trace["observability_gaps"] == []
    assert packet["coverage"]["semantic_coverage"] == 1.0
    assert len(packet["claims"]) == 1


def test_cross_domain_and_absolute_evidence_fail_closed() -> None:
    parent = load("agentic/registries/cohere_fast_workflow_contracts.yaml")
    children = load("agentic/registries/cohere_fast_subworkflows.yaml")
    bad = event("scope-and-ground", 1); bad["domain_id"] = "rh"
    try:
        assemble_cohere_fast_trace(parent, children, [bad], run_id="cf-live", domain_id="ym", target="yang-mills")
    except ValueError as exc:
        assert "cross-domain" in str(exc)
    else:
        raise AssertionError("cross-domain event accepted")
    bad = event("scope-and-ground", 1); bad["evidence"][0]["path"] = "/private/source.json"
    try:
        assemble_cohere_fast_trace(parent, children, [bad], run_id="cf-live", domain_id="ym", target="yang-mills")
    except ValueError as exc:
        assert "absolute" in str(exc)
    else:
        raise AssertionError("absolute evidence path accepted")
