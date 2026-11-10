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

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "agentic/spec/public_reasoning_event.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def complete_event(workflow_id: str, profile_id: str | None = None) -> dict:
    return {
        "schema_version": "2.0.0", "event_id": f"evt-{workflow_id}", "run_id": f"run-{workflow_id}",
        "workflow_id": workflow_id, "workflow_version": "1.0.0", "profile_id": profile_id,
        "target": "paper:example", "activation_receipt_id": "activation-1", "sequence": 1,
        "timestamp_utc": "2026-08-05T12:00:00+00:00", "phase": "analysis", "step_id": "step-1",
        "skill": "example-skill", "attempt": 1, "branch": None, "event_family": "public_inference",
        "causal_parent_event_ids": [], "parent_artifact_ids": [],
        "artifact_validation_status": "integrity_valid", "claim_epistemic_status": "conjectural",
        "workflow_disposition": "accepted",
        "public_inference": {
            "question": "Which bounded conclusion follows?",
            "premises": [{"type": "artifact", "statement": "A reviewed packet exists."}],
            "operator": "abduction", "warrant": "The packet supports this candidate within its stated scope.",
            "conclusion": "Retain the candidate for validation.", "assumptions": ["The packet is current."],
            "alternatives": [{"candidate": "reject", "disposition": "deferred", "reason": "falsifier pending"}],
            "falsifiers": ["Contradictory primary evidence"], "uncertainty": "Not a proof.",
            "scope": {"regime": "finite", "model": "example", "before": "finite", "after": "finite"},
            "trace_completeness": "complete"
        },
        "evidence": [{"relation": "supports", "path": "artifacts/example.json", "digest": None, "receipt_id": "receipt-1", "artifact_type": "Packet", "external": False}],
        "authority": {"exercised": ["workflow-step"], "absent": ["proof-acceptance"], "prohibitions_checked": ["no-scope-widening"]},
        "idempotency_key": "step-1-attempt-1"
    }


def test_contract_covers_every_named_workflow_and_route_a() -> None:
    registry = json.loads((ROOT / "agentic/registries/named_workflow_contracts.yaml").read_text())
    identities = [(row["id"], None) for row in registry["workflows"]]
    identities.append(("manuscript_result_elaboration", "route_a"))
    for workflow_id, profile_id in identities:
        VALIDATOR.validate(complete_event(workflow_id, profile_id))


def test_contract_rejects_missing_identity_absolute_local_path_and_malformed_handoff() -> None:
    missing = complete_event("proof")
    del missing["event_id"]
    assert list(VALIDATOR.iter_errors(missing))
    absolute = complete_event("proof")
    absolute["evidence"][0]["path"] = "/private/local/proof.json"
    assert list(VALIDATOR.iter_errors(absolute))
    malformed = complete_event("proof")
    malformed["handoff"] = {"destination_workflow_id": "review"}
    assert list(VALIDATOR.iter_errors(malformed))


def test_external_absolute_evidence_is_explicitly_allowed() -> None:
    external = copy.deepcopy(complete_event("review"))
    external["evidence"][0].update(path="/external/archive/item.json", external=True)
    VALIDATOR.validate(external)

