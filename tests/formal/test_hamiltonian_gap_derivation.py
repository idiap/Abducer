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


class HamiltonianGapDerivationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Exercise report construction from the preserved route-state fixture.
        # New production authority is checked by canonical acceptance tests.
        commands = [
            ["agentic/scripts/build_reasoning_event_log.py"],
            ["agentic/scripts/build_reasoning_monitor_packet.py"],
            ["agentic/scripts/generate_reasoning_monitor_html.py"],
            ["agentic/scripts/build_hamiltonian_gap_derivation.py"],
            ["agentic/scripts/generate_hamiltonian_gap_derivation_html.py"],
        ]
        for command in commands:
            subprocess.run([sys.executable, *command], cwd=ROOT, check=True)

    def test_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/validate_hamiltonian_gap_derivation.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_the_quoted_route_has_a_mathematical_derivation(self) -> None:
        report = json.loads((ROOT / "agentic/reports/hamiltonian_gap_derivation/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(report["report_mode"], "Hamiltonian spectral-gap mathematical derivation")
        derivation = report["derivations"][0]
        self.assertEqual(derivation["creative_operation"], "theorem_weakening")
        self.assertIn("bounded Hamiltonian spectral-gap route", derivation["route_text"])
        self.assertIn("reconstructed Yang-Mills objects", derivation["route_text"])
        formulas = " ".join(step["formula"] for step in derivation["derivation_steps"])
        for marker in [
            r"U(t)=e^{-itH}",
            r"P_\perp=I-P_0",
            r"E_H((0,\Delta))P_\perp=0",
            r"\langle\psi,H\psi\rangle",
            r"\ge\Delta\|\psi\|^2",
            r"C_A(t)=",
            r"e^{-\Delta t}",
            r"\liminf_{a\to0}\Delta_a\ge\Delta>0",
        ]:
            self.assertIn(marker, formulas)
        for step in derivation["derivation_steps"]:
            context = step["equation_context"]
            self.assertGreaterEqual(len(context["definitions"]), 2)
            self.assertTrue(context["assumptions_used"])
            self.assertGreaterEqual(len(context["valid_when"]), 2)
            context_text = json.dumps(context).lower()
            self.assertTrue(
                any(marker in context_text for marker in ["reconstructed", "spectral", "vacuum", "cutoff", "observable"]),
                context,
            )
        self.assertIn("spectral theorem", json.dumps(derivation).lower())
        self.assertIn("gauge-invariant", json.dumps(derivation).lower())
        self.assertGreaterEqual(len(derivation["what_would_count_as_progress"]), 4)
        for progress in derivation["what_would_count_as_progress"]:
            self.assertIn("claim", progress)
            self.assertIn("why", progress)
            self.assertGreaterEqual(len(progress["why"].split()), 18)
        progress_text = json.dumps(derivation["what_would_count_as_progress"]).lower()
        for marker in ["hamiltonian", "density", "cutoff", "continuum", "nontrivial", "interacting"]:
            self.assertIn(marker, progress_text)
        self.assertGreaterEqual(len(derivation["what_does_not_count"]), 4)

    def test_hamiltonian_route_points_to_derivation_artifact(self) -> None:
        packet = json.loads((ROOT / "agentic/reports/reasoning_monitor/latest.json").read_text(encoding="utf-8"))
        routes = [
            route
            for route in packet["candidate_routes"]
            if route.get("route_blueprint", {}).get("route_family") == "Hamiltonian spectral-gap route"
        ]
        self.assertTrue(routes)
        for route in routes:
            artifacts = route.get("route_blueprint", {}).get("derivation_artifacts", [])
            self.assertIn("agentic/reports/hamiltonian_gap_derivation/latest.html", artifacts)
            self.assertIn("agentic/reports/hamiltonian_gap_derivation/latest.md", artifacts)

    def test_derivation_html_renders_mathml(self) -> None:
        html = (ROOT / "agentic/reports/hamiltonian_gap_derivation/latest.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(html.count("<math"), 7)
        self.assertIn('<annotation encoding="application/x-tex">U(t)=e^{-itH}', html)
        self.assertIn('<annotation encoding="application/x-tex">E_H((0,\\Delta))P_\\perp=0', html)
        self.assertIn('<annotation encoding="application/x-tex">C_A(t)=', html)
        self.assertIn("Rendered Derivation", html)
        self.assertIn("Equation Context", html)
        self.assertIn("Assumptions used:", html)
        self.assertIn("Valid when:", html)
        self.assertIn("Why:", html)
        self.assertIn("progress-card", html)
        for forbidden in ["<script src=", "<link ", "http://", "https://", "@import", "<img "]:
            self.assertNotIn(forbidden, html.lower())


if __name__ == "__main__":
    unittest.main()
