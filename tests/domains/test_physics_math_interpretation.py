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

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PhysicsMathInterpretationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Exercise report construction from the preserved route-state fixture.
        # New production authority is checked by canonical acceptance tests.
        commands = [
            ["agentic/scripts/build_reasoning_event_log.py"],
            ["agentic/scripts/build_reasoning_monitor_packet.py"],
            ["agentic/scripts/generate_reasoning_monitor_html.py"],
            ["agentic/scripts/run_long_horizon_probe.py"],
            ["agentic/scripts/build_physics_math_interpretation.py"],
        ]
        for command in commands:
            subprocess.run([sys.executable, *command], cwd=ROOT, check=True)

    def test_interpretation_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/validate_physics_math_interpretation.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_active_routes_have_physics_math_anatomy(self) -> None:
        report = json.loads((ROOT / "agentic/reports/physics_math_interpretation/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(report["interpretation_mode"], "active physics/math route interpretation")
        self.assertIn("Numeric relevance scores are intentionally not used", report["not_a_score_policy"])
        families = {item["route_family"] for item in report["interpretations"]}
        self.assertIn("Balaban RG continuum-control route", families)
        self.assertIn("Euclidean correlator-decay to spectral-gap route", families)
        for item in report["interpretations"]:
            self.assertGreaterEqual(len(item["mathematical_objects"]), 3)
            self.assertGreaterEqual(len(item["mechanism_chain"]), 5)
            self.assertGreaterEqual(len(item["false_positive_controls"]), 3)
            self.assertGreaterEqual(len(item["next_lemma_questions"]), 3)
            text = json.dumps(item, sort_keys=True).lower()
            self.assertIn("not proof", text)
            self.assertTrue("reject" in text or "do not" in text)
            self.assertIn("hamiltonian", text)
            self.assertIn("continuum", text)

    def test_cross_route_synthesis_names_the_joint_problem(self) -> None:
        report = json.loads((ROOT / "agentic/reports/physics_math_interpretation/latest.json").read_text(encoding="utf-8"))
        synthesis = json.dumps(report["cross_route_synthesis"], sort_keys=True).lower()
        for marker in ["same limiting yang-mills theory", "rg", "correlator", "spectral", "os"]:
            self.assertIn(marker, synthesis)


if __name__ == "__main__":
    unittest.main()
