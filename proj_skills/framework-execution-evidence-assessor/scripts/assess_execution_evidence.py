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
"""Classify eligible runtime receipts without treating tests as executions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build(index: dict[str, Any]) -> dict[str, Any]:
    records = index.get("records", index.get("evidence", []))
    assessments, missing, contested = [], [], []
    for record in records:
        if record.get("kind") not in {"execution_receipt", "test"}:
            continue
        evidence_id = str(record.get("id", record.get("evidence_id", "")))
        if record.get("kind") == "test":
            missing.append(f"{evidence_id}: test source exists but no execution receipt is indexed")
            continue
        else:
            outcome = str(record.get("metadata", {}).get("outcome", record.get("outcome", "observed")))
            if outcome == "conflicting":
                status, caveat = "contested", "Conflicting receipt outcomes remain unresolved."
            elif record.get("metadata", {}).get("validator_receipt"):
                status, caveat = "verified", "Named validator receipt is linked."
            elif record.get("metadata", {}).get("replay_id"):
                status, caveat = "replayed", "Named replay receipt is linked."
            else:
                status, caveat = "observed", "A receipt was observed but not independently verified."
        if status == "contested":
            contested.append(evidence_id)
        assessments.append({"assessment_id": f"exec-{evidence_id}",
                            "subject_id": str(record.get("metadata", {}).get("subject_id") or evidence_id),
                            "status": status, "receipt_evidence_ids": [evidence_id],
                            "limitations": [caveat, "Does not establish frequency, cost, effectiveness, reachability, or generalization."]})
    if not assessments:
        assessments.append({"assessment_id": "exec-missing", "subject_id": "repository-workflow",
                            "status": "missing", "receipt_evidence_ids": [],
                            "limitations": ["No eligible execution receipts were indexed."]})
        missing.append("No eligible execution receipts were indexed.")
    raw_digest = str(index.get("digest", ""))
    source_digest = raw_digest if raw_digest.startswith("sha256:") and len(raw_digest) == 71 else digest(index)
    result = {"schema_version": "1.0.0", "model_id": "execution-evidence-model",
              "input_digest": source_digest, "assessments": assessments,
              "missing_evidence": missing, "contested_evidence": contested}
    result["model_digest"] = digest(result)
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
