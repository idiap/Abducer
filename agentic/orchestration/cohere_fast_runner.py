# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Abducer-native, filesystem-contained runner for cohere-fast."""
from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from typing import Callable

TERMINAL = {"failed", "quarantined", "stopped"}
ALLOWED_TRANSITIONS = {"created":{"running","stopped"}, "running":{"accepted","failed","quarantined","stopped"}, "failed":set(), "quarantined":set(), "stopped":set(), "accepted":set()}

def canonical_digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def _safe_child(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    resolved = root.resolve()
    if candidate != resolved and resolved not in candidate.parents:
        raise ValueError("artifact path escapes cohere-fast run root")
    return candidate

def transition(current: str, requested: str) -> str:
    if requested not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"invalid state transition: {current} -> {requested}")
    return requested

class CohereFastRunner:
    def __init__(self, artifact_root: Path, contracts: Path | None = None):
        self.artifact_root = artifact_root.resolve()
        path = contracts or Path(__file__).resolve().parents[1] / "registries/cohere_fast_subworkflows.yaml"
        self.contract = json.loads(path.read_text(encoding="utf-8"))

    def run(self, activation: dict, request: dict, executor: Callable[[dict, dict], dict], *, resume: dict | None = None) -> dict:
        if activation.get("receipt_type") != "cohere_fast_activation" or activation.get("workflow_id") != "cohere_fast":
            raise ValueError("valid cohere-fast activation receipt required")
        domain, run_id = activation["domain_id"], activation["run_id"]
        run_root = _safe_child(self.artifact_root, f"cohere-fast/{domain}/{run_id}")
        run_root.mkdir(parents=True, exist_ok=True)
        requested_child = activation.get("subworkflow_id")
        children = self.contract["subworkflows"]
        if requested_child:
            children = [c for c in children if c["id"] == requested_child]
            if not children: raise ValueError("unregistered child")
        prior = {r["step_id"]: r for r in (resume or {}).get("steps", []) if r.get("state") == "accepted"}
        receipts = []
        packet = dict(request)
        for child in children:
            if child["id"] in prior:
                receipts.append(prior[child["id"]]); continue
            if receipts and receipts[-1]["state"] in TERMINAL: break
            attempt = 0
            max_attempts = int(child.get("budget", {}).get("max_attempts", 1))
            while True:
                attempt += 1
                result = executor(dict(child), dict(packet))
                state = str(result.get("state", "failed"))
                if state != "failed" or attempt >= max_attempts:
                    break
            if state == "failed" and child.get("on_failure") in {"stop", "quarantine"}:
                state = "stopped" if child["on_failure"] == "stop" else "quarantined"
            if state not in {"accepted","failed","quarantined","stopped"}: raise ValueError("executor returned invalid state")
            artifacts = result.get("artifacts", {})
            digests = {}
            for relpath, content in artifacts.items():
                path = _safe_child(run_root, relpath)
                path.parent.mkdir(parents=True, exist_ok=True)
                raw = content if isinstance(content, bytes) else str(content).encode()
                fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                with os.fdopen(fd, "wb") as stream: stream.write(raw)
                digests[relpath] = "sha256:" + hashlib.sha256(raw).hexdigest()
            material = {"run_id":run_id,"step":child["id"],"attempt":attempt,"input":canonical_digest(packet),"state":state,"artifacts":digests}
            receipt_id = "cfr-" + hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()[:32]
            receipt = {"schema_version":"1.0.0","receipt_type":"step","receipt_id":receipt_id,"run_id":run_id,"workflow_id":"cohere_fast","domain_id":domain,"subworkflow_id":child["id"],"parent_run_id":activation.get("parent_run_id"),"step_id":child["id"],"attempt":attempt,"state":state,"input_digest":material["input"],"artifact_digests":digests}
            receipts.append(receipt)
            receipt_path = _safe_child(run_root, f"receipts/{child['id']}.json")
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
            packet = result.get("packet", packet)
        return {"run_id":run_id,"workflow_id":"cohere_fast","domain_id":domain,"state":receipts[-1]["state"] if receipts else "created","steps":receipts,"run_root":str(run_root)}
