#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Synthesize traceable paper-level constructs from three typed models."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def tex_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value.title()) or "Construct"


def synthesize(functional: dict[str, Any], workflow: dict[str, Any], execution: dict[str, Any]) -> tuple[dict[str, Any], str]:
    source_digests = {functional.get("input_digest"), workflow.get("input_digest"), execution.get("input_digest")}
    if None in source_digests or len(source_digests) != 1:
        raise ValueError("functional, workflow, and execution models must share one input digest")
    constructs = []
    reverse: dict[str, list[str]] = {}
    for capability in functional.get("capabilities", []):
        evidence = capability.get("evidence_ids", [])
        if not evidence:
            raise ValueError(f"capability {capability.get('id')} has no evidence")
        concrete_id = capability["capability_id"]
        cid = "construct-" + str(concrete_id).removeprefix("cap-")
        constructs.append({"construct_id": cid, "name": capability["name"],
                           "definition": capability["purpose"], "evidence_ids": evidence,
                           "retained_invariants": capability.get("invariants", []),
                           "omitted_details": ["file layout", "implementation-specific naming"],
                           "generalization_conditions": ["equivalent input, state, validation, and output contracts"],
                           "failure_conditions": capability.get("limitations", []) or ["underlying preconditions are not met"]})
        reverse.setdefault(concrete_id, []).append(cid)
    essential = {
        "gate": "control gate", "state_store": "persistent state", "artifact": "evidence-bearing artifact",
        "validator": "validation operator", "stage": "state transition stage",
    }
    for node in workflow.get("nodes", []):
        if node.get("node_type") not in essential:
            continue
        evidence = node.get("evidence_ids", [])
        if not evidence:
            raise ValueError(f"workflow node {node.get('id')} has no evidence")
        cid = f"construct-node-{node['node_id']}"
        constructs.append({"construct_id": cid, "name": essential[node["node_type"]],
                           "definition": f"An abstract {node['node_type']} preserving the indexed control semantics.",
                           "evidence_ids": evidence,
                           "retained_invariants": ["identity and evidence posture remain explicit"],
                           "omitted_details": ["repository path and presentation metadata"],
                           "generalization_conditions": ["the same control relation is preserved"],
                           "failure_conditions": ["the cited control relation is absent or bypassed"]})
        reverse.setdefault(node["node_id"], []).append(cid)
    feedback = [edge for edge in workflow.get("edges", []) if edge.get("edge_type") == "feeds_back_to"]
    posture = sorted({item.get("status", "unknown") for item in execution.get("assessments", [])})
    model = {
        "schema_version": "1.0.0", "model_id": "framework-abstraction-model",
        "input_digests": [functional.get("model_digest"), workflow.get("model_digest"), execution.get("model_digest")],
        "constructs": sorted(constructs, key=lambda item: item["construct_id"]),
        "state_space": ["workflow state", "evidence state", "validation state"],
        "operators": sorted({construct["name"] for construct in constructs}),
        "control_model": f"Typed workflow edges retain gates, handoffs, stops, and {len(feedback)} feedback loops.",
        "epistemic_semantics": "Declared topology and runtime execution evidence are orthogonal evidence categories.",
        "persistence_model": "State-store and persists-to relations preserve durable state when present in indexed evidence.",
        "governance_model": "Validators and gates bound transitions without establishing target-domain correctness.",
        "evaluation_status": ", ".join(posture) if posture else "unknown",
        "limitations": ["The abstraction describes indexed repository evidence, not framework efficacy or novelty."],
        "trace_links": [{"construct_id": cid, "concrete_ids": [concrete],
                         "evidence_ids": next(item["evidence_ids"] for item in constructs if item["construct_id"] == cid)}
                        for concrete, ids in sorted(reverse.items()) for cid in sorted(ids)],
    }
    model["model_digest"] = digest(model)
    lines = ["% Generated notation registry; do not edit."]
    for number, construct in enumerate(model["constructs"], 1):
        lines.append(f"\\newcommand{{\\{tex_name(construct['construct_id'])}}}{{\\mathcal{{C}}_{{{number}}}}}")
    return model, "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("functional_model", type=Path)
    parser.add_argument("workflow_model", type=Path)
    parser.add_argument("execution_model", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("notation", type=Path)
    args = parser.parse_args()
    values = [json.loads(path.read_text()) for path in (args.functional_model, args.workflow_model, args.execution_model)]
    model, notation = synthesize(*values)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.notation.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n")
    args.notation.write_text(notation)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
