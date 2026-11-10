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
"""Create an evidence-gated claim ledger; never generate paper prose."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def packet_authorized(packet: dict[str, Any] | None) -> bool:
    return bool(packet and packet.get("authorized") and packet.get("records"))


def curate(model: dict[str, Any], literature: dict[str, Any] | None = None,
           results: dict[str, Any] | None = None, candidates: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    claims = []
    for number, construct in enumerate(model.get("constructs", []), 1):
        evidence = construct.get("evidence_ids", [])
        if not evidence:
            raise ValueError(f"construct {construct.get('id')} has no evidence")
        claims.append({
            "claim_id": f"CL-DESCRIPTIVE-{number:03d}",
            "text": f"The indexed framework defines {construct['name']} as an explicit abstract construct.",
            "scope": "frozen indexed repository snapshot", "claim_class": "descriptive", "status": "declared",
            "evidence_ids": evidence, "counterevidence_ids": [], "assumptions": [],
            "limitations": ["This structural description does not establish runtime execution or effectiveness."],
            "allowed_verbs": ["defines", "declares", "represents", "organizes"],
            "allowed_sections": ["abstract", "method", "architecture", "implementation", "limitations", "conclusion"],
            "external_citation_required": False, "named_receipt_required": False,
            "freshness": "current", "resolution": "accepted",
        })
    for candidate in candidates or []:
        claim_class = candidate.get("class", "descriptive")
        reason = None
        if claim_class in {"novelty", "comparative"} and not packet_authorized(literature):
            reason = "novelty/comparative claim lacks authorized external literature"
        elif claim_class == "evaluative" and not packet_authorized(results):
            reason = "evaluative claim lacks authorized result receipts"
        elif candidate.get("basis") == "workflow_correctness" and candidate.get("asserts") == "proof_correctness":
            reason = "workflow correctness cannot establish target proof correctness"
        elif candidate.get("basis") == "topology" and candidate.get("asserts") == "runtime":
            reason = "declared topology cannot establish runtime execution"
        elif candidate.get("counterevidence") and not candidate.get("resolution"):
            reason = "unresolved counterevidence"
        if reason:
            number = len(claims) + 1
            claims.append({"claim_id": candidate.get("claim_id", f"CL-WITHHELD-{number:03d}"),
                           "text": candidate.get("text", candidate.get("exact_claim", "Withheld candidate claim")),
                           "scope": candidate.get("scope", "frozen indexed repository snapshot"),
                           "claim_class": claim_class, "status": "unknown",
                           "evidence_ids": candidate.get("evidence_ids", []),
                           "counterevidence_ids": candidate.get("counterevidence_ids", []),
                           "assumptions": candidate.get("assumptions", []), "limitations": [reason],
                           "allowed_verbs": ["may"], "allowed_sections": ["limitations"],
                           "external_citation_required": claim_class in {"novelty", "comparative"},
                           "named_receipt_required": claim_class == "evaluative",
                           "freshness": "unknown", "resolution": "withheld"})
        else:
            accepted = {"claim_id": candidate.get("claim_id", f"CL-CANDIDATE-{len(claims)+1:03d}"),
                        "text": candidate.get("text", candidate.get("exact_claim", "Accepted candidate claim")),
                        "scope": candidate.get("scope", "frozen indexed repository snapshot"),
                        "claim_class": claim_class, "status": candidate.get("status", "inferred"),
                        "evidence_ids": candidate.get("evidence_ids", []),
                        "counterevidence_ids": candidate.get("counterevidence_ids", []),
                        "assumptions": candidate.get("assumptions", []),
                        "limitations": candidate.get("limitations", []),
                        "allowed_verbs": candidate.get("allowed_verbs", ["suggests"]),
                        "allowed_sections": candidate.get("allowed_sections", ["limitations"]),
                        "external_citation_required": claim_class in {"novelty", "comparative"},
                        "named_receipt_required": claim_class == "evaluative",
                        "freshness": candidate.get("freshness", "current"), "resolution": "accepted"}
            claims.append(accepted)
    inputs = [model.get("model_digest") or digest(model)]
    if literature is not None:
        inputs.append(literature.get("digest") or digest(literature))
    if results is not None:
        inputs.append(results.get("digest") or digest(results))
    ledger = {"schema_version": "1.0.0", "ledger_id": "framework-paper-claim-ledger",
              "input_digests": sorted(set(inputs)), "claims": claims}
    ledger["ledger_digest"] = digest(ledger)
    return ledger


def load_optional(path: Path | None) -> dict[str, Any] | None:
    return json.loads(path.read_text()) if path else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("framework_model", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--literature", type=Path)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--candidates", type=Path)
    args = parser.parse_args()
    candidates = load_optional(args.candidates)
    if isinstance(candidates, dict):
        candidates = candidates.get("claims", [])
    ledger = curate(json.loads(args.framework_model.read_text()), load_optional(args.literature),
                    load_optional(args.results), candidates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
