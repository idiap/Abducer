# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Exercise explicitly imported extensions; native hook behavior is separate."""

from __future__ import annotations

import importlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]

hook_utils = importlib.import_module("hooks.workflow_local.hook_utils")
post_skill = importlib.import_module("hooks.workflow_local.post_skill_use_review")
pre_skill = importlib.import_module("hooks.workflow_local.pre_skill_use_policy")
stop_hook = importlib.import_module("hooks.workflow_local.stop_artifact_check")
prompt_hook = importlib.import_module("hooks.workflow_local.user_prompt_submit_intake")


class WorkflowLocalHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.registry = Path(self.tempdir.name) / "workflows.json"
        self.registry.write_text(
            json.dumps(
                {
                    "version": 2,
                    "workflows": [
                        {
                            "id": "proof_delivery",
                            "version": "1.2.0",
                            "target_scope": ["p-vs-np", "ym-*"],
                            "steps": [
                                {
                                    "id": "formalize",
                                    "order": 10,
                                    "skill": "proof-obligation-formalizer",
                                    "mode": "required",
                                    "produces": ["ProofPacket"],
                                },
                                {
                                    "id": "audit",
                                    "order": 20,
                                    "skill": "regime-shift-auditor",
                                    "mode": "conditional",
                                    "produces": ["AuditPacket"],
                                },
                            ],
                            "exit_gate": {
                                "required_artifacts": ["ProofPacket"],
                                "allowed": ["accepted", "quarantined"],
                                "open_obligations_policy": "forbid",
                            },
                            "profiles": [
                                {
                                    "id": "route_a",
                                    "version": "1.0.0",
                                    "aliases": ["routea"],
                                    "target_scope": ["manuscript:route-a"],
                                    "steps": [
                                        {
                                            "id": "routea_attack",
                                            "skill": "routea-paper-attack-orchestrator",
                                            "produces": ["RouteAAttackPlan"],
                                        }
                                    ],
                                    "specialist_skills": ["routea-geometric-collar-builder"],
                                    "specialist_output": "ResultCandidatePacket",
                                    "specialist_after": "routea_attack",
                                }
                            ],
                        },
                        {
                            "id": "paper_review",
                            "version": "1.0.0",
                            "target_scope": ["*"],
                            "steps": [{"id": "review", "skill": "paper-reviewer", "produces": ["Review"]}],
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.registry_patch = patch.object(hook_utils, "WORKFLOW_REGISTRY", self.registry)
        self.named_patch = patch.object(hook_utils, "NAMED_WORKFLOW_REGISTRY", Path(self.tempdir.name) / "absent.json")
        self.registry_patch.start()
        self.named_patch.start()

    def tearDown(self) -> None:
        self.named_patch.stop()
        self.registry_patch.stop()
        self.tempdir.cleanup()

    def run_hook(self, module: object, payload: dict) -> dict:
        stdout = io.StringIO()
        with (
            patch.object(sys, "stdin", io.StringIO(json.dumps(payload))),
            patch.object(module, "trace", lambda *_args: None),
            redirect_stdout(stdout),
        ):
            self.assertEqual(module.main(), 0)
        return json.loads(stdout.getvalue().strip().splitlines()[-1])

    @staticmethod
    def context(**overrides: object) -> dict:
        payload = {
            "controlled": True,
            "workflow_id": "proof_delivery",
            "workflow_version": "1.2.0",
            "target": "p-vs-np",
            "step_id": "formalize",
            "skill": "proof-obligation-formalizer",
        }
        payload.update(overrides)
        if "activation_receipt" not in overrides:
            payload["activation_receipt"] = hook_utils.make_activation_receipt(
                workflow_id=str(payload.get("workflow_id", "")),
                workflow_version=str(payload.get("workflow_version", "")),
                target=str(payload.get("target", "")),
                target_class=str(payload.get("target_class", "")),
                trigger_facts={"test_fixture": True},
                authorized_by="workflow-hook-test",
                evidence={"fixture": "synthetic contract"},
            )
        return payload

    def test_pre_skill_accepts_exact_workflow_target_step_membership(self) -> None:
        result = self.run_hook(pre_skill, self.context())
        self.assertEqual(result["decision"], "accept")

    def test_pre_skill_fails_closed_for_incomplete_or_borrowed_identity(self) -> None:
        cases = [
            self.context(workflow_id=""),
            self.context(workflow_version="9.0.0"),
            self.context(target="another-target"),
            self.context(skill="paper-reviewer"),
            self.context(skill="unknown-skill"),
            self.context(step_id="missing-step"),
        ]
        for payload in cases:
            with self.subTest(payload=payload):
                self.assertEqual(self.run_hook(pre_skill, payload)["decision"], "block")

    def test_conditional_step_requires_activation_evidence(self) -> None:
        conditional = self.context(step_id="audit", skill="regime-shift-auditor")
        self.assertEqual(self.run_hook(pre_skill, conditional)["decision"], "block")
        conditional["conditional_evidence"] = {"condition": "model boundary crossed", "artifact": "route-receipt"}
        self.assertEqual(self.run_hook(pre_skill, conditional)["decision"], "block")
        conditional["completed_steps"] = ["formalize"]
        self.assertEqual(self.run_hook(pre_skill, conditional)["decision"], "accept")

    def test_explicit_uncontrolled_invocation_remains_compatible(self) -> None:
        self.assertEqual(self.run_hook(pre_skill, {"controlled": False, "skill": "anything"})["decision"], "accept")

    def test_profile_steps_and_specialists_require_matching_activation(self) -> None:
        profile = self.context(
            profile_id="route_a",
            profile_version="1.0.0",
            target="manuscript:route-a",
            step_id="routea_attack",
            skill="routea-paper-attack-orchestrator",
        )
        self.assertEqual(self.run_hook(pre_skill, profile)["decision"], "block")
        profile["profile_activation_evidence"] = {"reason": "explicit Route A request"}
        self.assertEqual(self.run_hook(pre_skill, profile)["decision"], "accept")

        specialist = {
            **profile,
            "step_id": "specialist:routea-geometric-collar-builder",
            "skill": "routea-geometric-collar-builder",
            "completed_steps": ["routea_attack"],
        }
        self.assertEqual(self.run_hook(pre_skill, specialist)["decision"], "accept")
        self.assertEqual(
            self.run_hook(pre_skill, {**specialist, "skill": "paper-reviewer"})["decision"],
            "block",
        )

    def test_post_skill_validates_output_and_emits_deterministic_receipt(self) -> None:
        payload = self.context(
            output_type="ProofPacket",
            epistemic_status="candidate",
            expected_artifacts=["README.md"],
        )
        first = self.run_hook(post_skill, payload)
        second = self.run_hook(post_skill, payload)
        self.assertEqual(first["decision"], "accept")
        self.assertEqual(first["receipt"], second["receipt"])
        self.assertEqual(first["receipt"]["status"], "accepted")

        wrong_type = self.run_hook(post_skill, {**payload, "output_type": "Review"})
        missing = self.run_hook(post_skill, {**payload, "expected_artifacts": ["does-not-exist.json"]})
        self.assertEqual(wrong_type["decision"], "block")
        self.assertEqual(missing["decision"], "block")
        self.assertEqual(missing["receipt"]["status"], "rejected")

    def test_stop_uses_active_workflow_gate_and_open_obligations(self) -> None:
        payload = self.context(step_id=None, completed_artifacts=["ProofPacket"], gate_status="accepted", open_obligations=[])
        self.assertEqual(self.run_hook(stop_hook, payload)["decision"], "accept")
        self.assertEqual(self.run_hook(stop_hook, {**payload, "completed_artifacts": []})["decision"], "block")
        self.assertEqual(self.run_hook(stop_hook, {**payload, "open_obligations": ["prove lemma"]})["decision"], "block")

    def test_prompt_intake_is_advisory_only(self) -> None:
        for prompt in ("Systematically navigate this target", "Explain this definition"):
            result = self.run_hook(prompt_hook, {"prompt": prompt})
            self.assertNotEqual(result["decision"], "block")
            self.assertFalse(result["activation_authorized"])

    def test_prompt_trigger_matching_is_positive_negative_and_advisory_for_every_workflow(self) -> None:
        registry = json.loads((ROOT / "agentic/registries/named_workflow_contracts.yaml").read_text())
        with patch.object(hook_utils, "WORKFLOW_REGISTRY", ROOT / "agentic/registries/workflow_contracts.yaml"), patch.object(
            hook_utils,
            "NAMED_WORKFLOW_REGISTRY",
            ROOT / "agentic/registries/named_workflow_contracts.yaml",
        ):
            for workflow in registry["workflows"]:
                trigger = workflow["trigger"]
                positive = {fact: True for fact in [*trigger["all_of"], *trigger["any_of"]]}
                accepted = self.run_hook(prompt_hook, {"prompt": "", "trigger_facts": positive})
                ids = {row["workflow_id"] for row in accepted.get("workflow_recommendations", [])}
                self.assertIn(workflow["id"], ids)
                self.assertFalse(accepted["activation_authorized"])

                negative_cases = []
                missing_required = dict(positive)
                missing_required[trigger["all_of"][0]] = False
                negative_cases.append(missing_required)
                missing_alternative = dict(positive)
                for fact in trigger["any_of"]:
                    missing_alternative[fact] = False
                negative_cases.append(missing_alternative)
                prohibited = dict(positive)
                prohibited[trigger["none_of"][0]] = True
                negative_cases.append(prohibited)
                for negative in negative_cases:
                    rejected = self.run_hook(
                        prompt_hook, {"prompt": "", "trigger_facts": negative}
                    )
                    rejected_ids = {
                        row["workflow_id"]
                        for row in rejected.get("workflow_recommendations", [])
                    }
                    self.assertNotIn(workflow["id"], rejected_ids)


if __name__ == "__main__":
    unittest.main()
