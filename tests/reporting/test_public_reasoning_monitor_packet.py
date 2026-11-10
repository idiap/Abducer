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

import jsonschema


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from build_public_reasoning_monitor_packet import build_packet  # noqa: E402


def _fixture_trace() -> dict:
    return json.loads(
        (ROOT / "tests/fixtures/reasoning_trace/generated/theorem_proof_delivery.trace.json").read_text(encoding="utf-8")
    )


def test_monitor_packet_is_deterministic_and_schema_valid() -> None:
    lenses = json.loads((ROOT / "agentic/registries/reasoning_trace_lenses.yaml").read_text(encoding="utf-8"))
    first = build_packet(_fixture_trace(), lenses)
    second = build_packet(_fixture_trace(), lenses)
    assert first == second
    schema = json.loads((ROOT / "agentic/spec/public_reasoning_monitor_packet.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(first)


def test_packet_keeps_control_science_scope_and_authority_distinct() -> None:
    lenses = json.loads((ROOT / "agentic/registries/reasoning_trace_lenses.yaml").read_text(encoding="utf-8"))
    packet = build_packet(_fixture_trace(), lenses)
    assert packet["identity"]["workflow_id"] == "theorem_proof_delivery"
    assert packet["claims"]
    assert packet["evidence"]
    assert packet["scope_ledger"]
    assert packet["authority_ledger"]
    assert packet["obligations"]
    assert packet["coverage"]["semantic_covered_steps"] > 0
    assert all("epistemic_status" in claim and "integrity_status" in claim for claim in packet["claims"])
