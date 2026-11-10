#!/usr/bin/env python3
"""Fail-closed domain, lineage, and namespace policy for cohere-fast hooks."""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
BUNDLES = ROOT / "agentic/registries/domain_skill_bundles.yaml"
CHILDREN = ROOT / "agentic/registries/cohere_fast_subworkflows.yaml"

def _load(path: Path) -> dict: return yaml.safe_load(path.read_text(encoding="utf-8"))
def authorize(payload: dict) -> dict:
    activation = payload.get("activation_receipt")
    if not isinstance(activation, dict) or activation.get("receipt_type") != "cohere_fast_activation": return _blocked(payload, "activation receipt required")
    required = {"workflow_id","domain_id","run_id"}
    if any(payload.get(k) != activation.get(k) for k in required): return _blocked(payload, "workflow/domain/run binding mismatch")
    if payload.get("workflow_id") != "cohere_fast": return _blocked(payload, "cohere skills require cohere_fast workflow")
    bundles = {b["id"]:b for b in _load(BUNDLES).get("bundles", [])}
    bundle = bundles.get(payload["domain_id"])
    if not bundle: return _blocked(payload, "unregistered domain")
    feature_enabled = os.environ.get("ABDUCER_ENABLE_COHERE_FAST", "").lower() in {"1", "true", "yes"}
    if not bundle.get("enabled", True) and not feature_enabled: return _blocked(payload, "domain bundle disabled")
    allowed_skills = set(bundle.get("allowed_skills", bundle.get("skills", [])))
    skill = payload.get("skill")
    if skill and skill not in allowed_skills and skill != "cohere-fast-orchestrator": return _blocked(payload, "skill not authorized by domain bundle")
    child = payload.get("subworkflow_id")
    allowed_children = set(bundle.get("subworkflows", []))
    if child and child not in allowed_children: return _blocked(payload, "child not authorized by domain bundle")
    if child and not payload.get("parent_run_id"): return _blocked(payload, "child requires parent lineage")
    if payload.get("parent_event_id") and not str(payload["parent_event_id"]).startswith("evt-"): return _blocked(payload, "forged parent event")
    expected = f"cohere-fast/{payload['domain_id']}/{payload['run_id']}/"
    prefix = str(payload.get("artifact_prefix", ""))
    if prefix != expected: return _blocked(payload, "artifact namespace mismatch")
    return _receipt(payload, "accept", "domain, lineage, and namespace bindings accepted")

def _blocked(payload: dict, reason: str) -> dict: return _receipt(payload, "block", reason)
def _receipt(payload: dict, decision: str, reason: str) -> dict:
    material = {"decision":decision,"reason":reason,"workflow":payload.get("workflow_id"),"domain":payload.get("domain_id"),"run":payload.get("run_id"),"child":payload.get("subworkflow_id"),"parent":payload.get("parent_event_id")}
    rid = "cfh-" + hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()[:24]
    return {"schema_version":"1.0.0","receipt_id":rid,"decision":decision,"workflow_id":"cohere_fast","domain_id":str(payload.get("domain_id", "")),"run_id":str(payload.get("run_id", "")),"subworkflow_id":payload.get("subworkflow_id"),"parent_run_id":payload.get("parent_run_id"),"parent_event_id":payload.get("parent_event_id"),"artifact_prefix":str(payload.get("artifact_prefix", "")),"reason":reason}

def main() -> int:
    payload=json.loads(sys.stdin.read() or "{}")
    try: result=authorize(payload)
    except (OSError, json.JSONDecodeError, KeyError) as exc: result=_blocked(payload, f"policy input invalid: {exc}")
    print(json.dumps(result, sort_keys=True)); return 0
if __name__ == "__main__": raise SystemExit(main())
