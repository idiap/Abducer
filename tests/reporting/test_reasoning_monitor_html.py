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

"""Regression tests for the self-contained reasoning monitor HTML."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "agentic/reports/reasoning_monitor/latest.html"
PACKET = ROOT / "agentic/reports/reasoning_monitor/latest.json"


class ReasoningMonitorHtmlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Exercise the real CLI pipeline while restoring its checked-in reports
        # even if setup or assertions fail. SD headers and archived report bytes
        # must survive a test run so later REUSE/attribution checks are repeatable.
        reports = [
            ROOT / "agentic/reports" / directory / name
            for directory, names in (
                ("abstraction_chains", ("latest.json", "latest.md")),
                ("discovery_stretch", ("latest.json", "latest.md")),
                ("reasoning_monitor", ("latest.json", "latest.html")),
            )
            for name in names
        ]
        originals = {path: path.read_bytes() if path.exists() else None for path in reports}

        def restore_reports() -> None:
            for path, original in originals.items():
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(original)

        cls.addClassCleanup(restore_reports)
        subprocess.run([sys.executable, "agentic/scripts/build_abstraction_chain_packets.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "agentic/scripts/build_discovery_stretch.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "agentic/scripts/build_reasoning_monitor_packet.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "agentic/scripts/generate_reasoning_monitor_html.py"], cwd=ROOT, check=True)

    def _html(self) -> str:
        return HTML.read_text(encoding="utf-8")

    def _packet(self) -> dict:
        return json.loads(PACKET.read_text(encoding="utf-8"))

    def test_html_is_self_contained(self) -> None:
        text = self._html().lower()
        self.assertNotIn("<script src=", text)
        self.assertNotIn("<link ", text)
        self.assertNotIn("http://", text)
        self.assertNotIn("https://", text)
        self.assertNotIn("@import", text)
        self.assertNotIn("<img ", text)

    def test_embedded_packet_matches_active_target(self) -> None:
        text = self._html()
        match = re.search(r'<script id="monitor-data" type="application/json">(.*?)</script>', text, re.DOTALL)
        self.assertIsNotNone(match)
        embedded = json.loads(match.group(1))
        packet = self._packet()
        current = json.loads((ROOT / "agentic/state/current_target.json").read_text(encoding="utf-8"))
        self.assertEqual(embedded["target"]["target_id"], current["target_id"])
        self.assertEqual(embedded["target"]["target_id"], packet["target"]["target_id"])
        self.assertEqual(embedded["frontier"]["total"], packet["frontier"]["total"])
        self.assertEqual(embedded["reasoning_events"]["event_count"], packet["reasoning_events"]["event_count"])

    def test_required_controls_and_sections_exist(self) -> None:
        text = self._html()
        for dom_id in ["targetId", "goal", "metrics", "query", "laneFilter", "statusFilter", "commitmentFilter", "evidenceFilter", "view"]:
            self.assertIn(f'id="{dom_id}"', text)
        for tab in ["overview", "timeline", "frontier", "candidates", "strategy", "milestones", "reorientation", "subgoals", "machinery", "stretch", "debt", "evidence", "drift"]:
            self.assertIn(f'data-tab="{tab}"', text)
        for phrase in [
            "Target Spine",
            "Proof Debt",
            "Evidence Ledger",
            "Drift Guard",
            "Strategy Story",
            "Underlying mathematics",
            "Physics mechanism",
            "What Counts As A Physics Explanation",
            "What we learned",
            "Anti-Drift Rules",
            "Success Milestones",
            "Potentially Achieved When",
            "Certification Evidence",
            "Disqualifiers",
            "Reorientation Control",
            "Formal Subgoal Control",
            "Machinery Selection",
            "Large-Stretch Discovery Exploration",
            "Discovery Programs",
            "Falsifiers",
            "Promotion Signal",
            "Pivot Signal",
            "Universal Machinery Roles",
            "Controlled Interface",
            "Invalid Use Modes",
            "Yang-Mills Example Alignment",
            "Abstraction Chain",
            "Persist Or Adapt",
            "Learning From Failure",
            "Backtrack Trigger",
            "Pivot Trigger",
            "Quarantine Trigger",
            "Stop Condition",
            "Current Diagnosis",
            "Current Recommendation",
            "Bounded Reflection Contract",
            "Route-Level Diagnosis",
            "Decision Checkpoints",
            "Forbidden Shortcut",
        ]:
            self.assertIn(phrase, text)

    def test_packet_contains_visual_quality_surfaces(self) -> None:
        packet = self._packet()
        self.assertGreaterEqual(packet["frontier"]["total"], len(packet["frontier"]["items"]))
        self.assertGreater(packet["proof_obligations"]["total"], 0)
        self.assertGreater(len(packet["target_spine"]["commitment_ids"]), 0)
        self.assertEqual(packet["stale_workflow"]["critical_findings"], 0)
        self.assertTrue(packet["validation"]["active_target_match"])
        for route in packet["candidate_routes"][:4]:
            self.assertIn("target_relevance_score", route)
            self.assertIn("drift_risk", route)
            self.assertIn("subgoal_control", route)
            self.assertIn("machinery_selection", route)
            self.assertTrue(route["subgoal_control"]["target_object_link"])
            self.assertIn("->", route["machinery_selection"]["controlled_interface"])
            self.assertTrue(route["cited_commitment_ids"])

    def test_packet_contains_generative_strategy_story(self) -> None:
        story = self._packet()["interpretative_strategy_story"]
        self.assertEqual(story["title"], "Physics Strategy Story")
        self.assertGreaterEqual(len(story["story_beats"]), 4)
        story_text = json.dumps(story).lower()
        for marker in [
            "first we tried",
            "did not pay off",
            "then we moved",
            "balaban",
            "correlator",
            "hamiltonian",
            "what_we_learned",
            "gauge-field",
            "observable algebra",
            "spectral measure",
            "continuum limit",
            "same-theory transfer",
        ]:
            self.assertIn(marker, story_text)
        contract = story["physics_explanation_contract"]
        self.assertGreaterEqual(len(contract), 6)
        contract_text = " ".join(contract).lower()
        for marker in ["dynamical object", "scale story", "observables", "kinematics", "spectral meaning", "failure physically"]:
            self.assertIn(marker, contract_text)
        for beat in story["story_beats"]:
            self.assertTrue(beat["physics_story"])
            self.assertGreaterEqual(len(beat["what_we_learned"]), 2)
            self.assertTrue(
                any("learn" in item.lower() or "taught" in item.lower() or "shifted" in item.lower() for item in beat["what_we_learned"])
            )
            self.assertTrue(beat.get("why_it_did_not_pay_off") or beat.get("remaining_blockers") or beat.get("why_this_is_the_next_goal"))
            self.assertTrue(beat["equations"])
            for equation in beat["equations"]:
                self.assertTrue(equation["label"])
                self.assertTrue(equation["display"])

    def test_strategy_math_renderer_prefers_latex_and_covers_core_notation(self) -> None:
        text = self._html()
        self.assertIn("const source = eq.latex || eq.display || ''", text)
        for renderer_marker in [
            "\\\\operatorname",
            "\\\\mathrm",
            "\\\\mathcal",
            "\\\\varepsilon",
            "\\\\langle",
            "\\\\subseteq",
            "\\\\xrightarrow",
            "renderScripts",
            "normalizeMathSource",
            "math-arrow",
            "math-cal",
            "overline",
            "﹤",
        ]:
            self.assertIn(renderer_marker, text)

    def test_strategy_math_renderer_handles_angle_brackets_and_strict_inequalities(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node is not available for JavaScript renderer smoke test")
        source = (ROOT / "agentic/scripts/generate_reasoning_monitor_html.py").read_text(encoding="utf-8")
        start = source.index("function esc(value)")
        end = source.index("function pill(text")
        samples = [
            r"E_H((0,\Delta))P_\perp=0",
            r"\sum_{i,j}\overline c_i c_j S(\Theta f_i,f_j)<0",
            "<O_1 ... O_k>_c != 0",
            "&lt;O(t)O(0)&gt;_c &lt;= C_O exp(-m t)",
        ]
        script = (
            source[start:end]
            + "\nconst samples = "
            + json.dumps(samples)
            + ";\nconsole.log(JSON.stringify(samples.map(renderMathText)));\n"
        )
        result = subprocess.run(["node", "-e", script], cwd=ROOT, capture_output=True, text=True, check=True)
        rendered = json.loads(result.stdout)
        self.assertIn("P<sub>⊥</sub>=0", rendered[0])
        self.assertIn("﹤0", rendered[1])
        self.assertIn("⟨O<sub>1</sub> ... O<sub>k</sub>⟩<sub>c</sub> ≠ 0", rendered[2])
        self.assertIn("⟨O(t)O(0)⟩<sub>c</sub> ≤ C<sub>O</sub>", rendered[3])
        for item in rendered:
            self.assertNotIn("&lt;", item)
            self.assertNotIn("&gt;", item)

    def test_packet_contains_clear_success_milestones(self) -> None:
        milestones = self._packet()["success_milestones"]
        self.assertEqual(milestones["title"], "Success Milestones")
        self.assertGreaterEqual(len(milestones["items"]), 5)
        milestone_text = json.dumps(milestones).lower()
        for marker in ["big-deal", "potential breakthrough", "potentially achieved", "success signal", "certification", "disqualifiers"]:
            self.assertIn(marker, milestone_text)
        required_labels = [
            "Continuum Yang-Mills object constructed",
            "OS reconstruction yields the physical Hilbert space",
            "Cutoff-uniform Euclidean mass-gap witness obtained",
            "Positive Hamiltonian spectral gap proved",
            "Same-theory Clay target integration achieved",
        ]
        labels = {item["label"] for item in milestones["items"]}
        for label in required_labels:
            self.assertIn(label, labels)
        for milestone in milestones["items"]:
            self.assertTrue(milestone["why_big_deal"])
            self.assertTrue(milestone["potentially_achieved_when"])
            self.assertTrue(milestone["success_signal"])
            self.assertGreaterEqual(len(milestone["certification_evidence"]), 2)
            self.assertGreaterEqual(len(milestone["disqualifiers"]), 2)
            self.assertTrue(milestone["next_action"])

    def test_packet_contains_deep_reorientation_control(self) -> None:
        control = self._packet()["reorientation_control"]
        self.assertEqual(control["title"], "Reorientation Control")
        control_text = json.dumps(control).lower()
        for marker in [
            "restrategize",
            "backtrack",
            "pivot",
            "quarantine",
            "same-theory",
            "forbidden shortcut",
            "bounded reflection",
            "route-level",
            "yang-mills",
        ]:
            self.assertIn(marker, control_text)
        recommendation = control["current_recommendation"]
        self.assertEqual(recommendation["decision"], "restrategize_without_wholesale_pivot")
        self.assertTrue(recommendation["backtrack_guard"])
        self.assertTrue(recommendation["pivot_guard"])
        contract = control["bounded_reflection_contract"]
        self.assertGreater(contract["max_reflection_passes_before_action"], 0)
        self.assertGreaterEqual(len(contract["required_output_per_pass"]), 2)
        self.assertGreaterEqual(len(contract["stop_reflecting_when"]), 2)
        self.assertGreaterEqual(len(control["reorientation_modes"]), 4)
        self.assertGreaterEqual(len(control["decision_points"]), 3)
        self.assertGreaterEqual(len(control["active_reorientation_queue"]), 3)
        self.assertGreaterEqual(len(control["route_assessments"]), 1)
        self.assertIn("formal_subgoal_control_summary", control)
        for assessment in control["route_assessments"]:
            self.assertIn("subgoal_control", assessment)
            self.assertTrue(assessment["subgoal_control"]["learning_from_failure"])
        self.assertGreaterEqual(len(control["pivot_watchlist"]), 1)
        for mode in control["reorientation_modes"]:
            self.assertTrue(mode["deep_meaning"])
            self.assertTrue(mode["yang_mills_use"])
            self.assertTrue(mode["trigger"])
            self.assertTrue(mode["forbidden_shortcut"])
        for assessment in control["route_assessments"]:
            self.assertTrue(assessment["candidate_id"])
            self.assertTrue(assessment["recommended_move"])
            self.assertTrue(assessment["obstruction_type"])
            self.assertTrue(assessment["backtrack_trigger"])
            self.assertTrue(assessment["pivot_trigger"])
            self.assertTrue(assessment["next_probe"])
            self.assertTrue(assessment["protected_commitments"])
        for candidate in control["pivot_watchlist"]:
            self.assertTrue(candidate["candidate_id"])
            self.assertTrue(candidate["promotion_condition"])
        for point in control["decision_points"]:
            self.assertTrue(point["if_stalls"])
            self.assertTrue(point["backtrack_if"])
            self.assertTrue(point["pivot_if"])
            self.assertTrue(point["next_experiment"])
        for action in control["active_reorientation_queue"]:
            self.assertTrue(action["why_now"])
            self.assertTrue(action["success_condition"])

    def test_packet_contains_machinery_selection_section(self) -> None:
        packet = self._packet()
        machinery = packet["machinery_selection"]
        self.assertEqual(machinery["title"], "Machinery Selection")
        self.assertGreaterEqual(machinery["summary"]["selection_count"], len(packet["candidate_routes"]))
        self.assertIn("construction", machinery["policy"]["roles"])
        self.assertIn("transfer", machinery["policy"]["roles"])
        self.assertIn("witness", machinery["policy"]["roles"])
        chain = machinery["abstraction_chain"]
        self.assertGreaterEqual(len(chain["nodes"]), 6)
        self.assertGreaterEqual(len(chain["bridge_obligations"]), 5)
        for item in machinery["items"][:4]:
            self.assertTrue(item["target_object_link"])
            self.assertTrue(item["why_best_available"])
            self.assertTrue(item["machinery_not_yet_allowed"])
            self.assertIn("Yang-Mills", item["example_alignment"])
        for edge in chain["bridge_obligations"]:
            self.assertTrue(edge["bridge_obligation"])
            self.assertTrue(edge["failure_mode"])
            self.assertTrue(edge["validator_handoff"])

    def test_packet_contains_discovery_stretch_section(self) -> None:
        stretch = self._packet()["discovery_stretch"]
        self.assertEqual(stretch["quality_gate"], "pass")
        self.assertGreaterEqual(len(stretch["programs"]), 6)
        stretch_text = json.dumps(stretch).lower()
        for marker in ["reflection", "nontriviality", "observable density", "laplace", "mass scale", "no-gap"]:
            self.assertIn(marker, stretch_text)
        for program in stretch["programs"]:
            self.assertIn("->", program["controlled_interface"])
            self.assertGreaterEqual(len(program["equations"]), 2)
            self.assertGreaterEqual(len(program["falsifiers"]), 3)
            self.assertTrue(program["promotion_signal"])
            self.assertTrue(program["pivot_signal"])


if __name__ == "__main__":
    unittest.main()
