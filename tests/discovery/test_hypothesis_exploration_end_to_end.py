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
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class HypothesisExplorationEndToEndTests(unittest.TestCase):
    def test_pvsnp_fixture_covers_complex_route_pressure(self) -> None:
        fixture = json.loads((ROOT / "tests/fixtures/hegelian/p_vs_np_pressure_case.json").read_text(encoding="utf-8"))
        self.assertEqual(fixture["target"]["target_id"], "p-vs-np-target")
        pressure_types = {row["pressure_type"] for row in fixture["pressures"]}
        operations = {row["creative_operation"] for row in fixture["candidates"]}
        self.assertIn("failure", pressure_types)
        self.assertIn("discovery_signal", pressure_types)
        self.assertGreaterEqual(len(operations), 2)

    def test_small_math_fixture_requires_multiple_creative_operations(self) -> None:
        fixture = json.loads((ROOT / "tests/fixtures/hegelian/small_math_pressure_case.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(fixture["required_creative_operations"]), 2)
        self.assertIn("bridge_invention", fixture["required_creative_operations"])
        self.assertIn("theorem_weakening", fixture["required_creative_operations"])

    def test_refinement_trace_routes_blockers_to_actions(self) -> None:
        trace = json.loads((ROOT / "artifacts/hegelian/conceptual_refinement_trace.json").read_text(encoding="utf-8"))
        dispositions = {row["route_disposition"] for row in trace["cycles"]}
        self.assertTrue(dispositions & {"proof_queue", "discovery_branch", "revision_loop", "evidence_task", "quarantine"})
        self.assertIn("looper_gate_quarantine", trace["stop_conditions"])


if __name__ == "__main__":
    unittest.main()
