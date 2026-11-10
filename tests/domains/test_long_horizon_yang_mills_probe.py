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


class LongHorizonYangMillsProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Exercise report construction from the preserved route-state fixture.
        # New production authority is checked by canonical acceptance tests.
        commands = [
            ["agentic/scripts/build_reasoning_event_log.py"],
            ["agentic/scripts/build_abstraction_chain_packets.py"],
            ["agentic/scripts/build_reasoning_monitor_packet.py"],
            ["agentic/scripts/generate_reasoning_monitor_html.py"],
            ["agentic/scripts/run_long_horizon_probe.py"],
            ["agentic/scripts/build_yang_mills_bridge_lemma_packets.py"],
            ["agentic/scripts/build_big_deal_goal_archive.py"],
        ]
        for command in commands:
            subprocess.run([sys.executable, *command], cwd=ROOT, check=True)

    def test_probe_validates(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/validate_long_horizon_probe.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_active_proof_queue_is_budgeted_and_specific(self) -> None:
        report = json.loads((ROOT / "agentic/reports/long_horizon/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(report["quality_gate"], "pass")
        self.assertLessEqual(report["metrics"]["proof_queue_count"], report["metrics"]["proof_queue_budget"])
        self.assertEqual(report["metrics"]["proof_queue_count"], 2)
        for route in report["active_proof_queue"]:
            text = f"{route['transformation']} {route['source_witness']}".lower()
            self.assertNotIn("weaken the theorem-shaped obligation at `target:", text)
            self.assertNotIn("factor the opaque obligation", text)
            self.assertNotIn("smaller lemmas, evidence tasks, or discovery branches", text)
            self.assertGreaterEqual(route["target_relevance_score"], 0.8)
            self.assertGreaterEqual(len(route["domain_terms"]), 3)
            self.assertTrue(route["obligations"])
            self.assertTrue(route["route_family"])
            self.assertEqual(route["subgoal_control"]["decision"], "persist_adapt")
            self.assertTrue(route["subgoal_control"]["learning_from_failure"])
            self.assertTrue(route["subgoal_control"]["next_action"])
            self.assertIn("machinery_selection", route)
            self.assertNotEqual(route["machinery_selection"]["machinery_role"], "obstruction")
            self.assertIn("->", route["machinery_selection"]["controlled_interface"])
            self.assertTrue(route["machinery_selection"]["required_bridge_obligation"])
            physics_text = f"{route['physics_story']} {route['physical_failure_mode']}".lower()
            for marker in ["gauge", "continuum", "observable", "spectral"]:
                self.assertIn(marker, physics_text)
            self.assertTrue(any(term in text for term in ["balaban", "transfer matrix", "correlator", "renormalisation", "spectral"]))
            for obligation in route["obligations"]:
                self.assertFalse(obligation.startswith("Discharge `"), obligation)

    def test_active_proof_queue_covers_essential_commitments(self) -> None:
        report = json.loads((ROOT / "agentic/reports/long_horizon/latest.json").read_text(encoding="utf-8"))
        coverage = report["commitment_coverage"]
        self.assertEqual(coverage["missing"], [])
        self.assertIn("positive-mass-gap", coverage["active_proof_queue_union"])
        self.assertIn("continuum-limit", coverage["active_proof_queue_union"])
        self.assertIn("os-wightman-adequacy", coverage["active_proof_queue_union"])

    def test_skill_ecosystem_is_phase_coherent(self) -> None:
        report = json.loads((ROOT / "agentic/reports/long_horizon/latest.json").read_text(encoding="utf-8"))
        coherence = report["skill_ecosystem_coherence"]
        self.assertEqual(coherence["status"], "pass")
        self.assertEqual(coherence["critical_findings"], 0)
        self.assertGreaterEqual(coherence["metrics"]["projected_skill_count"], coherence["metrics"]["direct_workflow_skill_count"])
        phases = {phase["phase"]: phase for phase in coherence["phase_coverage"]}
        self.assertEqual(phases["target_navigation"]["status"], "role-complete")
        self.assertEqual(phases["conceptual_refinement"]["status"], "role-complete")
        self.assertIn("looper-target-goal-enricher", phases["target_navigation"]["composed_skills"])
        self.assertIn("abducer-mediation-candidate-generator", phases["conceptual_refinement"]["composed_skills"])
        self.assertTrue(phases["conditional_pools"]["review_pool"])
        self.assertTrue(phases["conditional_pools"]["ingest_pool"])
        self.assertTrue(phases["conditional_pools"]["reporting_pool"])
        policy = coherence["policy"].lower()
        for marker in ["phase-complete", "conditional", "control-plane", "discovery", "review"]:
            self.assertIn(marker, policy)

    def test_formal_subgoal_control_is_aggregated(self) -> None:
        report = json.loads((ROOT / "agentic/reports/long_horizon/latest.json").read_text(encoding="utf-8"))
        formal = report["formal_subgoal_control"]
        self.assertGreaterEqual(formal["summary"]["active_control_count"], report["metrics"]["candidate_routes"])
        self.assertEqual(formal["summary"]["stale_repeated_blockers"], [])
        self.assertGreaterEqual(formal["summary"]["decision_counts"]["persist_adapt"], report["metrics"]["proof_queue_count"])
        for control in formal["active_controls"]:
            self.assertIn(control["decision"], {"persist_adapt", "backtrack", "pivot", "quarantine", "stop"})
            self.assertTrue(control["target_object_link"])
            self.assertTrue(control["learning_from_failure"])

    def test_machinery_portfolio_is_aggregated(self) -> None:
        report = json.loads((ROOT / "agentic/reports/long_horizon/latest.json").read_text(encoding="utf-8"))
        machinery = report["machinery_portfolio"]
        self.assertGreaterEqual(machinery["summary"]["selection_count"], report["metrics"]["candidate_routes"])
        role_counts = machinery["summary"]["role_counts"]
        for role in ["construction", "transfer", "witness", "validation"]:
            self.assertGreaterEqual(role_counts.get(role, 0), 1, role)
        self.assertIn("RG construction", machinery["interpretation"])
        self.assertIn("correlator decay", machinery["interpretation"])
        for selection in machinery["active_selections"]:
            self.assertTrue(selection["selected_machinery"])
            self.assertTrue(selection["current_bottleneck"])
            self.assertTrue(selection["invalid_use_modes"])
            self.assertTrue(selection["validation_handoff"])

    def test_bridge_lemma_packets_continue_the_recursive_loop(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/validate_yang_mills_bridge_lemma_packets.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(report["target_id"], "yang-mills-existence-and-mass-gap-target")
        self.assertEqual(report["skill_coherence_status"], "pass")
        families = {packet["route_family"] for packet in report["packets"]}
        self.assertIn("Balaban RG continuum-control route", families)
        self.assertIn("Euclidean correlator-decay to spectral-gap route", families)
        for packet in report["packets"]:
            self.assertIn("same", packet["same_theory_invariant"].lower())
            self.assertGreaterEqual(len(packet["equations"]), 3)
            self.assertGreaterEqual(len(packet["failure_tests"]), 3)
            self.assertTrue(packet["conditional_skill_triggers"])
            for equation in packet["equations"]:
                self.assertIn("valid_when", equation)
                self.assertGreaterEqual(len(equation["valid_when"].split()), 10)

    def test_big_deal_goal_archive_is_armed_for_latex_and_paper_draft(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/validate_big_deal_goal_archive.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((ROOT / "agentic/reports/big_deal_goal_archive/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(report["target_id"], "yang-mills-existence-and-mass-gap-target")
        self.assertIn(report["archive_status"], {"armed_no_reached_goal", "activated"})
        self.assertIn("LaTeX process summary", report["trigger_policy"]["required_action"])
        self.assertIn("paper-argument draft", report["trigger_policy"]["required_action"])
        process_tex = ROOT / report["artifacts"]["process_summary_tex"]
        paper_tex = ROOT / report["artifacts"]["paper_argument_draft_tex"]
        self.assertTrue(process_tex.exists())
        self.assertTrue(paper_tex.exists())
        self.assertIn("Big-Deal Goal Process Summary", process_tex.read_text(encoding="utf-8"))
        self.assertIn("Physics Mechanism Learning", process_tex.read_text(encoding="utf-8"))
        paper_text = paper_tex.read_text(encoding="utf-8")
        self.assertIn("Argument Spine", paper_text)
        self.assertIn("Proof-Safety Boundary", paper_text)
        if report["reached_milestones"]:
            self.assertEqual(report["archive_status"], "activated")
            self.assertIn("Reached Milestones", paper_text)
        else:
            self.assertEqual(report["archive_status"], "armed_no_reached_goal")
            self.assertIn("No monitored milestone has reached", paper_text)

    def test_visible_monitor_routes_are_domain_specific(self) -> None:
        packet = json.loads((ROOT / "agentic/reports/reasoning_monitor/latest.json").read_text(encoding="utf-8"))
        markers = [
            "yang-mills",
            "yang mills",
            "balaban",
            "renormalisation",
            "renormalization",
            "schwinger",
            "wightman",
            "reflection positivity",
            "transfer matrix",
            "mass-gap",
            "mass gap",
            "spectral",
            "hamiltonian",
            "continuum",
            "gauge",
            "correlator",
        ]
        self.assertEqual(packet["target"]["target_id"], "yang-mills-existence-and-mass-gap-target")
        for route in packet["candidate_routes"]:
            text = route["proposed_transformation"].lower()
            self.assertNotIn("factor the opaque obligation", text)
            self.assertNotIn("smaller lemmas, evidence tasks, or discovery branches", text)
            self.assertTrue(route.get("route_blueprint", {}).get("route_family"), route["candidate_id"])
            self.assertTrue(any(marker in text for marker in markers), route["proposed_transformation"])
            for obligation in route.get("obligations", []):
                self.assertFalse(obligation.get("requirement", "").startswith("Discharge `"), obligation)


if __name__ == "__main__":
    unittest.main()
