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
"""Build a conservative functional capability IR from a frozen evidence index."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


IMPLEMENTATION_KINDS = {"implementation", "contract", "artifact"}
DECLARATION_KINDS = {"documentation", "history", "interpretation"}


def canonical_digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(data.encode()).hexdigest()


def valid_digest(value: Any, fallback: Any) -> str:
    text = str(value or "")
    return text if text.startswith("sha256:") and len(text) == 71 else canonical_digest(fallback)


def records(index: dict[str, Any]) -> list[dict[str, Any]]:
    return list(index.get("records", index.get("evidence", [])))


def semantic_group(record: dict[str, Any]) -> str:
    explicit = record.get("capability") or record.get("metadata", {}).get("capability")
    if explicit:
        return str(explicit).strip().lower().replace("_", "-").replace(" ", "-")
    path = str(record.get("path", "unknown")).lower()
    for key, group in (
        ("orchestrat", "orchestration-and-control"), ("reason", "reasoning"),
        ("evidence", "evidence-management"), ("valid", "validation"),
        ("report", "reporting"), ("persist", "state-persistence"),
        ("skill", "skill-execution"), ("test", "testing"),
    ):
        if key in path:
            return group
    return "framework-support"


def build(index: dict[str, Any]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records(index):
        evidence_id = record.get("id") or record.get("evidence_id")
        if evidence_id:
            grouped.setdefault(semantic_group(record), []).append(record)
    capabilities = []
    for name in sorted(grouped):
        items = sorted(grouped[name], key=lambda item: str(item.get("id", item.get("evidence_id"))))
        ids = [str(item.get("id", item.get("evidence_id"))) for item in items]
        kinds = {str(item.get("kind", "unknown")) for item in items}
        posture = "observed" if kinds & IMPLEMENTATION_KINDS else "declared"
        capabilities.append({
            "capability_id": f"cap-{name}", "name": name.replace("-", " ").title(),
            "purpose": f"Provide the evidence-backed {name.replace('-', ' ')} responsibility ({posture} posture).",
            "inputs": [], "outputs": [],
            "preconditions": [], "invariants": [],
            "components": sorted({str(item.get("path", "")) for item in items if item.get("path")}),
            "dependencies": [],
            "validators": [item_id for item_id, item in zip(ids, items) if item.get("kind") in {"test", "execution_receipt"}],
            "limitations": (["Only declaration-level evidence is available."] if posture == "declared" else []),
            "evidence_ids": ids,
        })
    source_digest = valid_digest(index.get("digest"), index)
    result = {"schema_version": "1.0.0", "model_id": "functional-capability-model",
              "input_digest": source_digest, "capabilities": capabilities,
              "limitations": ["Capabilities describe indexed evidence; they do not establish efficacy or runtime frequency."]}
    result["model_digest"] = canonical_digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_index", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build(json.loads(args.evidence_index.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
