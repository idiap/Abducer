#!/usr/bin/env python3
"""Deterministic, explicit-only cohere-fast invocation parser."""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "agentic/registries/domain_skill_bundles.yaml"
WORKFLOWS = ROOT / "agentic/registries/cohere_fast_workflow_contracts.yaml"

def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def parse_invocation(command: str, *, target: str) -> dict:
    tokens = command.strip().split()
    if not tokens or tokens[0] != "cohere-fast":
        raise ValueError("explicit cohere-fast alias required")
    if len(tokens) not in {2, 3}:
        raise ValueError("expected: cohere-fast <domain> [subworkflow]")
    if not target.strip():
        raise ValueError("target is required")
    domains = {r["id"]: r for r in _load(REGISTRY).get("bundles", [])}
    domain = domains.get(tokens[1])
    feature_enabled = os.environ.get("ABDUCER_ENABLE_COHERE_FAST", "").lower() in {"1", "true", "yes"}
    if not domain or (not domain.get("enabled", True) and not feature_enabled):
        raise ValueError("unknown or disabled domain")
    subworkflow = tokens[2] if len(tokens) == 3 else None
    allowed = set(domain.get("subworkflows", []))
    if subworkflow is not None and subworkflow not in allowed:
        raise ValueError("unknown subworkflow for domain")
    workflow_version = _load(WORKFLOWS)["workflow"]["version"]
    material = {"command": tokens, "target": target.strip(), "version": workflow_version}
    canonical = json.dumps(material, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    return {"schema_version":"1.0.0", "receipt_type":"cohere_fast_activation", "id":f"cfact-{digest[:24]}",
            "workflow_id":"cohere_fast", "workflow_version":workflow_version, "domain_id":tokens[1],
            "subworkflow_id":subworkflow, "target":target.strip(), "run_id":f"cf-{digest[24:48]}",
            "command_digest":f"sha256:{digest}"}

def main() -> int:
    payload = json.loads(sys.stdin.read() or "{}")
    try: print(json.dumps({"decision":"accept", "activation_receipt":parse_invocation(str(payload.get("command", "")), target=str(payload.get("target", "")))}, sort_keys=True))
    except (ValueError, OSError, json.JSONDecodeError) as exc: print(json.dumps({"decision":"block", "reason":str(exc)}, sort_keys=True))
    return 0
if __name__ == "__main__": raise SystemExit(main())
