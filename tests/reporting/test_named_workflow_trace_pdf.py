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

from validate_public_reasoning_trace_pdf import EXPECTED_STEMS, companion_paths, validate_set


def test_exactly_seven_realistic_pdf_companion_sets_validate() -> None:
    assert {p.name.removesuffix(".packet.json") for p in (ROOT / "tests/fixtures/reasoning_trace/generated").glob("*.packet.json")} == EXPECTED_STEMS
    for stem in sorted(EXPECTED_STEMS):
        paths = companion_paths(stem)
        assert all(path.is_file() for path in paths.values()), stem
        assert validate_set(paths) == [], stem


def test_route_a_retains_full_specialist_topology() -> None:
    paths = companion_paths("manuscript_result_elaboration-route_a")
    packet = json.loads(paths["packet"].read_text(encoding="utf-8"))
    inventory = json.loads(paths["inventory"].read_text(encoding="utf-8"))
    assert len(packet["declared_route"]) == 22
    assert len(packet["inferences"]) == 21
    assert len(packet["graph"]["edges"]) == 143
    assert len(inventory["semantic_ids"]["declared_route"]) == 22
    assert len(inventory["semantic_ids"]["inferences"]) == 21

